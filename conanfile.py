from conans import ConanFile, tools
import os


class SysConfigOpenGLConan(ConanFile):
    name = "sysconfig-opengl"
    version = "0.0.1"
    description = "cross-platform virtual conan package for the OpenGL support"
    topics = ("conan", "opengl", "gl")
    url = "https://github.com/bincrafters/conan-sysconfig-opengl"
    homepage = "https://www.opengl.org/"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["LICENSE"]
    settings = ("os",)

    def source(self):
        # download OpenGL headers from the Khronos Registry https://www.khronos.org/registry/OpenGL/index_gl.php
        for directory in ["GL", 'KHR', "EGL", "GLES", "GLES2", "GLES3"]:
            os.makedirs(directory)

        def _download(url, sha256):
            from six.moves.urllib.parse import urlparse
            filename = os.path.basename(urlparse(url).path)
            tools.download(url, filename)
            tools.check_sha256(filename, sha256)

        with tools.chdir("GL"):
            _download("https://www.khronos.org/registry/OpenGL/api/GL/glext.h",
                      "3e7f19e54717473a8882050b00ed982dc59fe929afcab6c4beb19891d5cf784a")
            _download("https://www.khronos.org/registry/OpenGL/api/GL/glcorearb.h",
                      "68e25c8ff756195574b6e329b4666c205c5f5a26b4632a5ffd9f377631655f65")
            _download("https://www.khronos.org/registry/OpenGL/api/GL/glxext.h",
                      "c1386ade12a9ea0986eb1e3ac8038d08ef4b5dd31949047905a458f22787457c")
            _download("https://www.khronos.org/registry/OpenGL/api/GL/wglext.h",
                      "f581bd8340b3a41abc07c4b0144537cab76bc6ad759ae4929ec2159d336a988b")

        with tools.chdir("KHR"):
            _download("https://www.khronos.org/registry/EGL/api/KHR/khrplatform.h",
                      "bbca133eec0bd0b62fc6f8d27d993aedda3c79f0de8ad3637f8cf42ffbeb8e7b")

        with tools.chdir("EGL"):
            _download("https://www.khronos.org/registry/EGL/api/EGL/egl.h",
                      "70207b48ccd7257473ae7517c2a9cab3f8268e073df303e58df66a2ac171f75c")
            _download("https://www.khronos.org/registry/EGL/api/EGL/eglext.h",
                      "5045357621c4c0729e6f3c425788a5837dcfdcb09d256cb7e9f96918fb2836a0")
            _download("https://www.khronos.org/registry/EGL/api/EGL/eglplatform.h",
                      "bce59928d5b82d5ed799c291d273d6f8fe44428beffcb48556ad90a23ac7754f")

        with tools.chdir("GLES"):
            _download("https://www.khronos.org/registry/OpenGL/api/GLES/gl.h",
                      "2f1d453d859f4e73a02ae720b962198c0adea91492ddc6f9404e764e18671845")
            _download("https://www.khronos.org/registry/OpenGL/api/GLES/glext.h",
                      "ae395b86cb96f325b526cfc5bbde4e0c17f411f8c74f554f8219d093d31f0cba")
            _download("https://www.khronos.org/registry/OpenGL/api/GLES/glplatform.h",
                      "857bf0685ecb0dddf692157ea9ef98c95e9f58b5ed0c41b26fd3fe51ed1a3624")
            _download("https://www.khronos.org/registry/OpenGL/api/GLES/egl.h",
                      "1ba84c782436b5e103cd1ee8060840846b96ec4727d00944cee59d1c44db0dda")

        with tools.chdir("GLES2"):
            _download("https://www.khronos.org/registry/OpenGL/api/GLES2/gl2.h",
                      "64fae5ff4a48463468be60439ea5869ebcb77cc80306538cad28ebb8e0a04299")
            _download("https://www.khronos.org/registry/OpenGL/api/GLES2/gl2ext.h",
                      "551e4082c1630e784a2397b64c748b3575ff43e200bd1658aca207f68d919828")
            _download("https://www.khronos.org/registry/OpenGL/api/GLES2/gl2platform.h",
                      "8f25443c4c5b3c8e702c3510f12b6ec8c23c2e3c1ca1c71bb07d148653696d9a")

        with tools.chdir("GLES3"):
            _download("https://www.khronos.org/registry/OpenGL/api/GLES3/gl3.h",
                      "b71b52974d2fdb2ccf49632bfb13f262f979c2179d0dd4f4b7718d2521065e17")
            _download("https://www.khronos.org/registry/OpenGL/api/GLES3/gl31.h",
                      "7fb6d736b3e2a4036f279e654230f6cd04ddfb564f5505c39036316fe40c9e94")
            _download("https://www.khronos.org/registry/OpenGL/api/GLES3/gl32.h",
                      "a2cfd7d890f16f67665e01e6f514a7c75bfc702e50c8861a44d04536271fffd1")
            _download("https://www.khronos.org/registry/OpenGL/api/GLES2/gl2ext.h",
                      "551e4082c1630e784a2397b64c748b3575ff43e200bd1658aca207f68d919828")
            _download("https://www.khronos.org/registry/OpenGL/api/GLES3/gl3platform.h",
                      "b4595aafef1eb9b4705cf8a69e29aadb8eb8e3dd3baf8b34ab702c9174dcb549")

    def package_id(self):
        self.info.header_only()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=".")
        self.copy(pattern="*.h", dst="include", src=".", keep_path=True)

    def package_info(self):
        if self.settings.os == "Macos":
            self.cpp_info.defines.append("GL_SILENCE_DEPRECATION=1")
            self.cpp_info.exelinkflags.append("-framework OpenGL")
            self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags
        elif str(self.settings.os) in ["iOS", "watchOS", "tvOS"]:
            self.cpp_info.exelinkflags.append("-framework OpenGLES")
            self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags
        elif self.settings.os == "Android":
            self.cpp_info.libs = ["EGL", "GLESv2"]
        elif self.settings.os == "Windows":
            self.cpp_info.libs = ["OpenGL32.lib"]
        elif self.settings.os == "Linux":
            # TODO: use libglvnd
            pass
