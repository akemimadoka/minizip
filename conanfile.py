from conans import ConanFile, CMake, tools

Options = [ ("MZ_COMPAT", True), ("MZ_ZLIB", True), ("MZ_BZIP2", True), ("MZ_LZMA", True),
    ("MZ_PKCRYPT", True), ("MZ_WZAES", True), ("MZ_LIBCOMP", False), ("MZ_OPENSSL", False),
    ("MZ_BRG", False), ("MZ_COMPRESS_ONLY", False), ("MZ_DECOMPRESS_ONLY", False),
    ("MZ_BUILD_TEST", False), ("MZ_BUILD_UNIT_TEST", False), ("MZ_BUILD_FUZZ_TEST", False) ]

class MinizipConan(ConanFile):
    name = "minizip"
    version = "2.8.9"
    license = "zlib"
    author = "nmoinvaz"
    url = "https://github.com/akemimadoka/minizip"
    topics = ("C++")
    settings = "os", "compiler", "build_type", "arch"

    options = {"shared": [True, False]}
    options.update({ opt[0] : [True, False] for opt in Options })
    
    default_options = ["shared=False"]
    default_options.extend([ "{}={}".format(opt[0], opt[1]) for opt in Options ])
    default_options = tuple(default_options)

    generators = "cmake"

    exports_sources = "lib*", "test*", "LICENSE", "CMakeLists.txt", "minizip.pc.cmakein", "*.c", "*.h"

    def requirements(self):
        if self.options.MZ_ZLIB:
            self.requires("zlib/1.2.11@conan/stable")
        if self.options.MZ_BZIP2:
            self.requires("bzip2/1.0.8@conan/stable")
        if self.options.MZ_OPENSSL:
            self.requires("OpenSSL/1.1.1d@conan/stable")
        if not self.settings.os in ["Windows", "WindowsStore", "WindowsCE"]:
            self.requires("libiconv/1.15@bincrafters/stable")

    def configure_cmake(self):
        cmake = CMake(self)

        cmake.definitions["BUILD_SHARED_LIBS"] = "ON" if self.options.shared else "OFF"
        for opt in Options:
            cmake.definitions[opt[0]] = getattr(self.options, opt[0])

        cmake.configure()
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
