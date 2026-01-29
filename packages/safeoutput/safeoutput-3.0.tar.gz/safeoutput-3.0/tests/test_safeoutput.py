import inspect
import tempfile
from os import remove
from os.path import dirname, isfile

import pytest
import safeoutput


def _filename():
    return u"testfile_" + inspect.stack()[1][3]


def ensure_file_absent(path):
    try:
        remove(path)
    except OSError:
        pass


def expected_file(path, expected, cleanup=True):
    if isinstance(expected, str):
        mode = "r"
    else:
        mode = "rb"
    try:
        if expected is not None:
            with open(path, mode) as f:
                content = f.read()
                return content == expected
        else:
            return False == isfile(path)
    finally:
        if cleanup:
            ensure_file_absent(path)

def test_file_with_success_str():
    file_data = u"testoutput"
    mode = "w"
    expect_success(file_data, mode)

def test_file_with_success_bytes():
    file_data = u"testoutput".encode('utf-8')
    mode = "wb"
    expect_success(file_data, mode)

def expect_success(file_data, mode):
    file_name = _filename()
    ensure_file_absent(file_name)
    with safeoutput.open(file_name, mode) as f:
        f.write(file_data)
    assert expected_file(file_name, file_data)


def test_with_exception():
    file_name = _filename()
    file_data = u"testoutput"
    ensure_file_absent(file_name)
    try:
        with safeoutput.open(file_name) as f:
            f.write(file_data)
            raise ValueError(u"We eff'ed up")
    except ValueError:
        pass
    assert expected_file(file_name, None)


def test_close_success():
    file_name = _filename()
    file_data = u"testoutput"
    ensure_file_absent(file_name)
    f = safeoutput.open(file_name)
    f.write(file_data)
    f.close()
    assert expected_file(file_name, file_data)


def test_close_exception():
    file_name = _filename()
    file_data = u"testoutput"
    ensure_file_absent(file_name)

    def write():
        f = safeoutput.open(file_name)
        f.write(file_data)
        raise ValueError(u"We eff'ed up")

    try:
        write()
    except ValueError:
        pass
    assert expected_file(file_name, None)


def test_write_after_close():
    file_name = _filename()
    file_data = u"testoutput"
    ensure_file_absent(file_name)
    f = safeoutput.open(file_name)
    f.write(file_data)
    f.close()
    assert expected_file(file_name, file_data, False)
    with pytest.raises(ValueError):
        f.write(file_data)
    assert expected_file(file_name, file_data)

def test_write_stdout_after_close(capsys):
    file_data = u"testoutput"
    f = safeoutput.open(None)
    f.write(file_data)
    f.close()
    f.write(file_data)
    out,err = capsys.readouterr()
    assert out == file_data + file_data
    assert err == ""

def test_stdout_with_success_str(capsys):
    file_data = u"testoutput"
    mode = "w"
    with safeoutput.open(None, mode) as f:
        f.write(file_data)
    out,err = capsys.readouterr()
    assert out == file_data
    assert err == ""


def test_stdout_with_success_bytes(capsys):
    file_data = b"testoutput"
    with safeoutput.open(None, "wb") as f:
        f.write(file_data)
    out, err = capsys.readouterr()
    assert out.encode() == file_data
    assert err == ""


def test_custom_usedir():
    file_data = "testoutput"
    with tempfile.TemporaryDirectory() as tmpdir:
        # Output file in current dir, but tempfile should be in tmpdir
        file_name = _filename()
        ensure_file_absent(file_name)
        try:
            with safeoutput.open(file_name, useDir=lambda _: tmpdir) as f:
                # Verify tempfile is in the custom directory
                assert dirname(f.name) == tmpdir
                f.write(file_data)
            assert expected_file(file_name, file_data, cleanup=False)
        finally:
            ensure_file_absent(file_name)


def test_flush():
    file_name = _filename()
    file_data = "testoutput"
    ensure_file_absent(file_name)
    try:
        with safeoutput.open(file_name) as f:
            f.write(file_data)
            f.flush()
            # After flush, data should be in tempfile (not yet renamed)
            with open(f.name, "r") as tmp:
                assert tmp.read() == file_data
    finally:
        ensure_file_absent(file_name)


def test_name_property():
    file_name = _filename()
    ensure_file_absent(file_name)
    try:
        with safeoutput.open(file_name) as f:
            # name should be the tempfile path, not the destination
            assert f.name != file_name
            assert isfile(f.name)
        # After close, the tempfile is renamed to destination
        assert isfile(file_name)
    finally:
        ensure_file_absent(file_name)


def test_close_with_explicit_rollback():
    file_name = _filename()
    file_data = "testoutput"
    ensure_file_absent(file_name)
    f = safeoutput.open(file_name)
    f.write(file_data)
    f.close(commit=False)
    # File should not exist after explicit rollback
    assert not isfile(file_name)


def test_atomic_rename():
    file_name = _filename()
    file_data = "testoutput"
    ensure_file_absent(file_name)
    try:
        with safeoutput.open(file_name) as f:
            f.write(file_data)
            f.flush()
            # Destination should not exist while context manager is open
            assert not isfile(file_name)
            # But tempfile should exist
            assert isfile(f.name)
        # After exiting context, destination should exist
        assert isfile(file_name)
    finally:
        ensure_file_absent(file_name)


def test_multiple_writes():
    file_name = _filename()
    ensure_file_absent(file_name)
    try:
        with safeoutput.open(file_name) as f:
            f.write("line1\n")
            f.write("line2\n")
            f.write("line3\n")
        assert expected_file(file_name, "line1\nline2\nline3\n", cleanup=False)
    finally:
        ensure_file_absent(file_name)


def test_large_multiline_content():
    file_name = _filename()
    ensure_file_absent(file_name)
    # Generate 10000 lines of content
    file_data = "\n".join(f"line {i}: {'x' * 100}" for i in range(10000)) + "\n"
    try:
        with safeoutput.open(file_name) as f:
            f.write(file_data)
        assert expected_file(file_name, file_data, cleanup=False)
    finally:
        ensure_file_absent(file_name)


def test_unicode_content():
    file_name = _filename()
    ensure_file_absent(file_name)
    # Test various unicode: emoji, CJK, Arabic, accented chars
    file_data = "Hello 世界! مرحبا 🎉 café naïve 日本語\n"
    try:
        with safeoutput.open(file_name) as f:
            f.write(file_data)
        assert expected_file(file_name, file_data, cleanup=False)
    finally:
        ensure_file_absent(file_name)


def test_binary_mode_exception():
    file_name = _filename()
    file_data = b"binary data"
    ensure_file_absent(file_name)
    try:
        with safeoutput.open(file_name, "wb") as f:
            f.write(file_data)
            raise ValueError("Error during binary write")
    except ValueError:
        pass
    # File should not exist after exception in binary mode
    assert not isfile(file_name)


def test_getattr_delegation():
    file_name = _filename()
    ensure_file_absent(file_name)
    try:
        with safeoutput.open(file_name) as f:
            f.write("test")
            # Test that file methods are delegated via __getattr__
            assert hasattr(f, "readable")
            assert hasattr(f, "writable")
            assert hasattr(f, "seekable")
            # writable should return True for a tempfile
            assert f.writable()
    finally:
        ensure_file_absent(file_name)
