import pytest
from src.media_indexing.folder_index import Folder, remove_artist, remove_counter, get_folders, get_updated_media_paths, apply_new_media_paths, reindex_folders

@pytest.fixture
def sample_folder(tmp_path):

    folder1 = tmp_path / "Artist A (3)"
    folder1.mkdir()
    (folder1 / "track1 [Artist A].mp3").touch()
    (folder1 / "track2 [Artist A].mp3").touch()
    (folder1 / "track3 [Artist A].mp3").touch()

    folder2 = tmp_path / 'Empty Folder (0)'
    folder2.mkdir()

    folder3 = tmp_path / 'Single Artist (1)'
    folder3.mkdir()
    (folder3 / 'song.flac').touch()

    folder4 = tmp_path / 'No Counter'
    folder4.mkdir()

    (folder4 / 'track.mp3').touch()

    folder5 = tmp_path / 'VA (3)'
    folder5.mkdir()
    (folder5 / 'track1.mp3').touch()
    (folder5 / 'track2.mp3').touch()
    (folder5 / 'track3.mp3').touch()


    return tmp_path

def test_remove_counter():
    assert remove_counter('Artist (5)') == 'Artist'

def test_folder_init(sample_folder):
    folder_path = sample_folder / 'Artist A (3)'
    folder = Folder(folder_path)

    assert folder_path == folder.path
    assert  folder.title == 'Artist A'



def test_get_media_list(sample_folder):
    folder_path = sample_folder / "Artist A (3)"
    folder = Folder(folder_path)
    media_list = folder.get_media_list()
    assert  len(media_list) == 3

def test_remove_artist_rem():
    assert remove_artist("Song1 [ArtistA]") == "Song1"


def test_get_counter_empty_folder(sample_folder):
    empty_folder = sample_folder / "Empty Folder (0)"
    folder = Folder(empty_folder)
    assert folder.get_counter() == 0

def test_get_counter_with_files(sample_folder):
    folder = sample_folder / "Artist A (3)"
    folder = Folder(folder)
    assert folder.get_counter() == 3


def test_get_folders(sample_folder):
    folders = get_folders(sample_folder)
    assert len(folders) == 5
    assert all(isinstance(f, Folder) for f in folders)

def test_rename_file(sample_folder):
    folder = sample_folder / "Artist A (3)"
    folder = Folder(folder)
    folder.rename_with_counter()

def test_get_new_folder_name(sample_folder):
    folder = Folder(sample_folder / "Artist A (3)")
    assert  folder.get_new_folder_name() == "Artist A (3)"

    folder.title = 'New Name'
    assert folder.get_new_folder_name() == 'New Name (3)'

def test_rename_with_counter(sample_folder):
    folder_path = sample_folder / 'No Counter'
    folder = Folder(folder_path)

    origin_path = folder.path
    folder.rename_with_counter()

    assert folder.path.name == 'No Counter (1)'
    assert folder.path.exists()

def test_va_folder_creation(sample_folder):
    folders = get_folders(sample_folder)
    va_folder = next((f for f in folders if 'VA' in f.path.name), None)

    assert va_folder is not None
    assert va_folder.get_counter() == 3


def test_case_sensitivity(sample_folder):
    case_folder = next((f for f in get_folders(sample_folder) if 'Empty Folder' in f.path.name), None)
    assert case_folder is not None


def test_get_media_list(sample_folder):
    folder_path = sample_folder / "Artist A (3)"
    folder = Folder(folder_path)
    media_list = folder.get_media_list()
    assert len(media_list) == 3
    assert all(m.path.suffix == ".mp3" for m in media_list)

def test_folder_init_title(sample_folder):
    folder = Folder(sample_folder / "Artist A (3)")
    assert folder.title == "Artist A"
    folder2 = Folder(sample_folder / "No Counter")
    assert folder2.title == "No Counter"


def test_get_counter(sample_folder):
    folder = Folder(sample_folder / "VA (3)")
    assert folder.get_counter() == 3

    empty_folder = Folder(sample_folder / "Empty Folder (0)")
    assert empty_folder.get_counter() == 0

def test_remove_counter_removes_suffix():
    assert remove_counter("My Folder (5)") == "My Folder"
    assert remove_counter("No Counter") == "No Counter"

def test_get_updated_media_paths(sample_folder):
    mapping = get_updated_media_paths(sample_folder)
    assert all(p != mapping[p] for p in mapping)
    assert all("[Artist" not in str(dst) for dst in mapping.values())









def test_get_updated_media_paths(sample_folder):
    mapping = get_updated_media_paths(sample_folder)

    assert isinstance(mapping, dict)
    assert all(str(k) != str(v) for k, v in mapping.items())
    assert all(".mp3" in str(v) or ".flac" in str(v) for v in mapping.values())

def test_apply_new_media_paths(sample_folder):
    mapping = get_updated_media_paths(sample_folder)
    apply_new_media_paths(mapping)

    for old_path in mapping:
        assert not old_path.exists()
    for new_path in mapping.values():
        assert new_path.exists()


from src.media_indexing.folder_index import Media

def test_media_init_raises_on_directory(tmp_path):
    folder = tmp_path / "some_folder"
    folder.mkdir()
    with pytest.raises(ValueError, match="is a dir"):
        Media(folder)


def test_folder_init_raises_on_file(tmp_path):
    file = tmp_path / "file.mp3"
    file.touch()
    with pytest.raises(ValueError, match="is not a dir"):
        Folder(file)


def test_reindex_folders(sample_folder):
    folders = [Folder(p) for p in sample_folder.iterdir() if p.is_dir()]
    reindex_folders(folders)
    for folder in folders:
        assert folder.path.exists()
        assert "(" in folder.path.name





'''
def test_artist_brackets_in_filename_after_rename(sample_folder):
    folder_path = sample_folder / "Artist A (3)"
    folder = Folder(folder_path)
    media_list = folder.get_media_list()

    for media in media_list:
        media.rename_update()
        assert f"[{media.artist_name}]" in media.path.name
'''
#def test_s_sensitivity(sample_folder):
#    folder_path = sample_folder / 'Artist A (3)'
#    f = Folder(folder_path)
#    case_folder = next((f for f in  f.get_media_list() if '[' in f), None)