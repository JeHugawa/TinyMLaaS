/* Copyright 2019 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

#include "detection_responder.h"
#include <cmath>
#include "tensorflow/lite/micro/micro_log.h"

// This dummy implementation writes person and no person scores to the error
// console. Real applications will want to take some custom action instead, and
// should implement their own versions of this function.
void RespondToDetection(float person_score, float no_person_score) {
  float person_score_frac, person_score_int;
  float no_person_score_frac, no_person_score_int;
  person_score_frac = std::modf(person_score * 100, &person_score_int);
  no_person_score_frac = std::modf(no_person_score * 100, &no_person_score_int);
  MicroPrintf("Person score: %d.%d%% No person score: %d.%d%%",
              static_cast<int>(person_score_int),
              static_cast<int>(person_score_frac * 100),
              static_cast<int>(no_person_score_int),
              static_cast<int>(no_person_score_frac * 100));

}
