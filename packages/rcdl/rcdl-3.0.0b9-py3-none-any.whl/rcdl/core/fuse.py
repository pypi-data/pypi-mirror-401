# core/fuse.py

"""Handle merging videos from a same post"""

import os
import subprocess

from rcdl.core.config import Config
from rcdl.core.db import DB
from rcdl.core.models import FusedStatus, Status, FusedMedia, Media, Post
from rcdl.interface.ui import UI
import rcdl.core.downloader_subprocess as dls
from rcdl.utils import get_media_metadata, get_date_now


def update_db(fuse: FusedMedia, medias: list[Media], user: str, result):
    """Update DB depending on subprocess result (SUCESS/FAILURE)"""
    if result == 0:
        path = os.path.join(Config.creator_folder(user), fuse.file_path)
        duration, file_size, checksum = get_media_metadata(path)
        fuse.duration = duration
        fuse.status = FusedStatus.FUSED
        fuse.checksum = checksum
        fuse.created_at = get_date_now()
        fuse.file_size = file_size
        for media in medias:
            media.status = Status.FUSED
    else:
        fuse.fail_count += 1
    with DB() as db:
        db.update_fuse(fuse)
        for media in medias:
            db.update_media(media)


def get_medias_and_post(
    post_id: str, total_parts: int
) -> tuple[None, None] | tuple[list[Media], Post]:
    """Get medias and post related to a fuse group.
    Return a list[Media] and a Post
    Handle Errors, return None, None"""
    # get associated post
    with DB() as db:
        post = db.query_post_by_id(post_id)
    if post is None:
        UI.error(f"Could not match fuses post id {post_id} to a post in post tables")
        return None, None

    # get all videos of a post
    with DB() as db:
        medias = db.query_media_by_post_id(post_id)

    # check number of media in db match total part expected in fused media
    if len(medias) != total_parts:
        UI.error(f"Found {len(medias)} videos part. Expected {total_parts}")
        return None, None

    # check all video are downloaded
    allowed_status = [Status.DOWNLOADED, Status.OPTIMIZED]
    if Config.DEBUG:
        allowed_status.append(Status.FUSED)
    ok = True
    for media in medias:
        if media.status not in allowed_status:
            ok = False
            break
    if not ok:
        return None, None

    # sort medias list
    sorted_medias = sorted(medias, key=lambda m: m.sequence)
    return sorted_medias, post


def fuse_medias():
    """Fuse all media part of a fuse group with status PENDING in DB fuses"""
    # get all fused media
    with DB() as db:
        fuses = db.query_fuses_by_status(FusedStatus.PENDING)
    if Config.DEBUG:
        with DB() as db:
            ok_fuses = db.query_fuses_by_status(FusedStatus.FUSED)
        fuses.extend(ok_fuses)

    with UI.progress_total_concat() as progress:
        task = progress.add_task("Total concat", total=len(fuses))

        for fm in fuses:
            medias, post = get_medias_and_post(fm.id, fm.total_parts)
            if medias is None or post is None:
                progress.advance(task)
                continue

            # concat medias
            result = 1
            try:
                result = dls.ffmpeg_concat(medias, post)
            except (OSError, subprocess.SubprocessError, ValueError) as e:
                UI.error(f"Failed to concat video (id:{post.id}) due to: {e}")

            # update db
            update_db(fm, medias, post.user, result)

            progress.update(
                task, advance=1, description=f"Concated media for id {fm.id}"
            )

            # remove part file
            for media in medias:
                media_full_path = os.path.join(
                    Config.creator_folder(post.user), media.file_path
                )
                try:
                    if Config.DEBUG:
                        UI.info(f"Skipped '{media_full_path}' removal")
                        continue
                    os.remove(media_full_path)
                    UI.info(f"Removed file '{media_full_path}'")
                except (FileNotFoundError, PermissionError) as e:
                    UI.error(
                        f"FileNotFound/PermissionError: Failed to "
                        f"remove media '{media_full_path}' due to: {e}"
                    )
                except OSError as e:
                    UI.error(f"Failed to remove media '{media_full_path}' due to: {e}")
