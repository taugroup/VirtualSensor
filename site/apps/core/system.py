import os, errno, shutil
import logging
import re
import codecs
import subprocess

from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from glob import glob
from django.http import HttpResponse
from django.template.loader import render_to_string
from settings.settings import MEDIA_ROOT

logger = logging.getLogger(__name__)


# make a file structure tree in Json
def make_tree(path):
    tree = dict(name=os.path.basename(path), children=[])
    try:
        lst = os.listdir(path)
    except OSError:
        pass  # ignore errors
    else:
        for name in lst:
            fn = os.path.join(path, name)
            if os.path.isdir(fn):
                tree['children'].append(make_tree(fn))
            else:
                tree['children'].append(dict(name=name))
    return tree


def mkdir_p(path):
    try:
        logger.info("mkdir -p %s" % path)
        os.makedirs(path, 0o777)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST:
            logger.info('dir already exists.')
            pass
        else:
            raise


def rename(pfrom, pto):
    try:
        logger.info("mv %s %s" % (pfrom, pto))
        shutil.move(pfrom, pto)
    except:
        raise


def rmdir(dir):
    logger.info("rm -r %s" % (dir))
    shutil.rmtree(dir, ignore_errors=True)


def render_to_file(filename, template, context):
    codecs.open(filename, 'w', 'utf-8').write(render_to_string(template, context))


# create symbolic links under dst_dir for all files under src_dir
def symlink_all(src_dir, dst_dir):
    # make sure we have dst_dir ready;
    mkdir_p(dst_dir)
    # create symbolic links to
    for src_path in glob("%s/*" % src_dir):
        try:
            os.symlink(os.path.abspath(src_path), os.path.join(dst_dir, os.path.basename(src_path)))
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST:
                logger.warn("symlink already exists.")
                pass
            else:
                raise


def exportfile(fin_name=None, fout_name=None, content_type=None):
    fsock = open(fin_name, 'r')
    response = HttpResponse(fsock, content_type=content_type)
    response["Content-Disposition"] = "attachment; filename=%s" % fout_name
    return response


def order_name(name):
    """order_name -- Limit a text to 20 chars length, if necessary strips the
    middle of the text and substitute it for an ellipsis.
    name -- text to be limited.
    """
    name = re.sub(r'^.*/', '', name)
    if len(name) <= 20:
        return name
    return name[:10] + "..." + name[-7:]


def serialize(instance, file_attr='file'):
    """serialize -- Serialize a file instance into a dict.
    instance -- file instance
    file_attr -- attribute name that contains the FileField or ImageField
    """
    obj = getattr(instance, file_attr)
    return {
        'url': obj.url,
        'name': order_name(obj.name),
        'size': obj.size,
        # 'deleteUrl': reverse('appinputdata_delete', args=[instance.app_input.pk,instance.pk]),
        # 'deleteType': 'DELETE',
        # 'deleteWithCredentials': True,
    }


def response_mimetype(request):
    if "application/json" in request.META['HTTP_ACCEPT']:
        return "application/json"
    else:
        return "text/plain"


# only works with input and file models
def get_upload_to(instance, filename):
    return os.path.join(instance.folder, filename)


def get_object_or_none(instance):
    try:
        o = instance.get_object()
    except ObjectDoesNotExist:
        o = None
    return o


def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""

    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False

    return user_passes_test(in_groups)


def exec(cmd, cwd, block=True):
    try:
        p = subprocess.Popen(cmd, cwd=cwd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if block:
            output = p.communicate()
            if output[1]:
                logger.error(output[1])

    except Exception:
        pass


# create symbolic links under dst_dir for all files under src_dir
def symlink_all(src_dir, dst_dir):
    # make sure we have dst_dir ready;
    mkdir_p(dst_dir)
    # create symbolic links to
    for src_path in glob("%s/*" % src_dir):
        try:
            os.symlink(os.path.abspath(src_path), os.path.join(dst_dir, os.path.basename(src_path)))
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST:
                logger.warning("symlink already exists.")
                pass
            else:
                raise
