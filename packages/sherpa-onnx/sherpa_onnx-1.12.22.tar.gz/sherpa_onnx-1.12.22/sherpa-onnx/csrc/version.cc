// sherpa-onnx/csrc/version.h
//
// Copyright      2025  Xiaomi Corporation

#include "sherpa-onnx/csrc/version.h"

namespace sherpa_onnx {

const char *GetGitDate() {
  static const char *date = "Thu Jan 15 03:15:38 2026";
  return date;
}

const char *GetGitSha1() {
  static const char *sha1 = "d081fbbc";
  return sha1;
}

const char *GetVersionStr() {
  static const char *version = "1.12.22";
  return version;
}

}  // namespace sherpa_onnx
