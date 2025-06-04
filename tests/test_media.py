import pytest
from src.media_indexing.folder_index import get_artist, remove_artist, Media

@pytest.fixture
def sample_media(tmp_path):
    def _create_file(name):
        f = tmp_path / name
        f.touch()
        return Media(f)
    return _create_file

def test_get_artist():
    assert get_artist('song1 [Artist B]') == 'Artist B'
    assert get_artist('track1 [Artist A]') == 'Artist A'
    assert get_artist('jazz_track2 [Artist C]') == 'Artist C'


def test_remove_artist():
    assert remove_artist('song1 [Artist B]') == 'song1'

def test_get_artist_multiple_artists():
    with pytest.raises(ValueError):
        get_artist("Song1 [ArtistA] [ArtistB]")

def test_media_init(sample_media):
    media = sample_media('track1 [Artist A].mp3')
    assert media.artist_name == 'Artist A'
    assert media.title == 'track1'

def test_media_rename_init(sample_media):
    media = sample_media('track1 [Artist A].mp3')
    media.title = 'track2'
    media.rename_update()
    assert media.path.name == 'track2 [Artist A].mp3'
