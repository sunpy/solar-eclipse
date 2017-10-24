from eclipse import SAMPLE_PHOTO
from eclipse import meta
import exifread

def test_sample_photo_date():
    tags = exifread.process_file(open(SAMPLE_PHOTO, 'rb'))
    result = meta.get_meta_from_exif(tags)
    assert result.get('DATEOBS') is not None

