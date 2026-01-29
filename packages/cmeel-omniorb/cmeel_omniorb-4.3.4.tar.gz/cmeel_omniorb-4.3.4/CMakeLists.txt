cmake_minimum_required(VERSION 3.30)

set(NAME omniorb)
set(VERSION 4.3.4)
set(EXT tar.bz2)
set(SHA256 79720d415d23cd8da99287a4ef4da0aa1bd34d3e4c7b1530715600adc5ed3dc3)

project("cmeel-${NAME}" VERSION "${VERSION}")

if(APPLE)
  set(ORIGIN "@loader_path")
  set(BUILD "")
else()
  set(ORIGIN "\$\$ORIGIN")
  set(BUILD "--build=${CMAKE_HOST_SYSTEM_PROCESSOR}-unknown-linux-gnu")
endif()

include(ExternalProject)
ExternalProject_Add(
  ${NAME}
  URL "http://downloads.sourceforge.net/${NAME}/omniORB-${VERSION}.${EXT}"
  URL_HASH "SHA256=${SHA256}"
  DOWNLOAD_EXTRACT_TIMESTAMP ON
  BUILD_IN_SOURCE ON
  CONFIGURE_COMMAND
    ${CMAKE_COMMAND} "-E" "env" "LDFLAGS=-Wl,-rpath,'${ORIGIN}'" "--"
    "./configure" "--prefix=${CMAKE_INSTALL_PREFIX}" "${BUILD}"
  BUILD_COMMAND "make"
  # TEST_COMMAND "make" "check"
  INSTALL_COMMAND "make" "install"
  COMMAND "sed" "-i.bak" "s=^#!.*python.*$=#!/usr/bin/env python="
          "${CMAKE_INSTALL_PREFIX}/bin/omniidl"
  COMMAND ${CMAKE_COMMAND} "-E" "rm" "${CMAKE_INSTALL_PREFIX}/bin/omniidl.bak")

# dummy file for install target
install(FILES "README.md" DESTINATION "share/cmeel-${NAME}/")
