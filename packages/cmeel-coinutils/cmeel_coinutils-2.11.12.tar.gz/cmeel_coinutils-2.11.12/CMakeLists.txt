cmake_minimum_required(VERSION 3.30)

set(ORG coin-or)
set(NAME CoinUtils)
set(VERSION "2.11.12")
set(EXT tar.gz)
set(SHA256 eef1785d78639b228ae2de26b334129fe6a7d399c4ac6f8fc5bb9054ba00de64)
set(TAG_PREFIX releases/)

project("cmeel-${NAME}" VERSION ${VERSION})

if(DEFINED ENV{CMEEL_JOBS})
  set(CMEEL_JOBS
      $ENV{CMEEL_JOBS}
      CACHE STRING "number of build jobs" FORCE)
else()
  set(CMEEL_JOBS
      4
      CACHE STRING "number of build jobs")
endif()

include(ExternalProject)
ExternalProject_Add(
  ${NAME}
  URL "https://github.com/${ORG}/${NAME}/archive/refs/tags/${TAG_PREFIX}${VERSION}.${EXT}"
  URL_HASH "SHA256=${SHA256}"
  DOWNLOAD_EXTRACT_TIMESTAMP OFF
  BUILD_IN_SOURCE ON
  CONFIGURE_COMMAND "./configure" "--prefix=${CMAKE_INSTALL_PREFIX}"
  BUILD_COMMAND "make" "-j${CMEEL_JOBS}"
  TEST_COMMAND "make" "check"
  INSTALL_COMMAND "make" "install"
  COMMAND "${CMAKE_COMMAND}" "-E" "rm"
          "${CMAKE_INSTALL_PREFIX}/lib/lib${NAME}.la")

# dummy file for install target
install(FILES README.md DESTINATION share/cmeel-${NAME}/)
