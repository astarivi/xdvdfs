import harness
import os

NAME_LEN = 18
FILE_BYTE_COUNT = 0xe + NAME_LEN
assert FILE_BYTE_COUNT == 32

def rand_file_name():
    import string
    import random
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(NAME_LEN))

class EmptyFile(harness.PackTestCase):
    def __init__(self):
        super().__init__(name='EmptyFile')

    def set_up(self, dir):
        with open(dir + '/empty_file', 'w') as f:
            pass

class EmptyRoot(harness.PackTestCase):
    def __init__(self):
        super().__init__(name='EmptyRoot')

    def set_up(self, dir):
        pass

class EmptySubdir(harness.PackTestCase):
    def __init__(self):
        super().__init__(name='EmptySubdir')

    def set_up(self, dir):
        os.mkdir(dir + '/subdir')

class SpecialCharsInName(harness.PackTestCase):
    def __init__(self):
        super().__init__(name='SpecialCharsInName')

    def create_file(self, dir, name):
        with open(dir + '/' + name, 'w') as f:
            f.write(name)

    def set_up(self, dir):
        self.create_file(dir, 'Ü')
        self.create_file(dir, 'b')
        self.create_file(dir, 'ü')
        self.create_file(dir, 'á')

class ManyFiles(harness.PackTestCase):
    def __init__(self):
        super().__init__(name='ManyFiles')


    def set_up(self, dir):
        os.mkdir(dir + '/a')
        max_offset = 65536
        num_files = max_offset // FILE_BYTE_COUNT + 1
        for i in range(num_files):
            name = rand_file_name()
            with open(dir + '/a/' + name, 'w') as f:
                f.write('data')

class DirentSize2048(harness.PackTestCase):
    def __init__(self):
        super().__init__(name='DirentSize2048')

    def set_up(self, dir):
        os.mkdir(dir + '/a')
        with open(dir + '/b', 'w') as f:
            f.write('data')

        for i in range(2048 // FILE_BYTE_COUNT):
            name = rand_file_name()
            with open(dir + '/a/' + name, 'w') as f:
                f.write('data')

class BuildImage(harness.BuildImageTestCase):
    def __init__(self):
        super().__init__(
                name='BuildImage',
                build_image_opts='-m bin:/ -m assets/**:/{0} -m **/*.always:/always/{2} -m a/specific.ext1:/specific.ext1 -m **/*.{ext1,ext2}:/{3}/{2} -m !**/excluded -m assets/excluded:assets/excluded'
                )

    def create_file(self, source_path, dest_path, data):
        with open(source_path, 'w') as f:
            f.write(data)
        if not dest_path:
            return
        with open(dest_path, 'w') as f:
            f.write(data)

    def set_up(self, dir):
        super().set_up(dir)

        os.mkdir(dir + '/source/bin')
        os.mkdir(dir + '/source/assets')
        os.mkdir(dir + '/source/a')
        os.mkdir(dir + '/source/b')
        os.mkdir(dir + '/source/src')

        os.mkdir(dir + '/dest/assets')
        os.mkdir(dir + '/dest/ext1')
        os.mkdir(dir + '/dest/ext2')
        os.mkdir(dir + '/dest/always')

        self.create_file(dir + '/source/bin/default.xbe', dir + '/dest/default.xbe', 'default.xbe')
        self.create_file(dir + '/source/assets/asset1', dir + '/dest/assets/asset1', 'asset1')
        self.create_file(dir + '/source/assets/asset2', dir + '/dest/assets/asset2', 'asset2')
        self.create_file(dir + '/source/assets/excluded', dir + '/dest/assets/excluded', 'excluded')
        self.create_file(dir + '/source/a/specific.ext1', dir + '/dest/specific.ext1', 'specific.ext1')
        self.create_file(dir + '/source/a/file1.ext1', dir + '/dest/ext1/file1', 'file1.ext1')
        self.create_file(dir + '/source/b/file2.ext1', dir + '/dest/ext1/file2', 'file2.ext1')
        self.create_file(dir + '/source/a/file1.ext2', dir + '/dest/ext2/file1', 'file1.ext2')
        self.create_file(dir + '/source/b/file2.ext2', dir + '/dest/ext2/file2', 'file2.ext2')
        self.create_file(dir + '/source/a/file.always', dir + '/dest/always/file', 'file.always')
        self.create_file(dir + '/source/a/excluded', None, 'excluded')
        self.create_file(dir + '/source/b/excluded', None, 'excluded')
