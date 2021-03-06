/*
 * Copyright (c) 2014-2016, Siemens AG. All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice,
 * this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 * this list of conditions and the following disclaimer in the documentation
 * and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */

#ifndef BASE_C_TEST_ALLOC_TEST_H_
#define BASE_C_TEST_ALLOC_TEST_H_

#include <partest/partest.h>
#include <vector>

namespace embb {
namespace base {
namespace test {

class AllocTest : public partest::TestCase {
 public:
  /**
   * Adds test methods.
   */
  AllocTest();

 private:
  /**
   * Tests non-aligned memory allocation and freeing with several threads.
   */
  void TestNonAlignedAlloc();
  void PostNonAligned();

  /**
   * Tests aligned memory allocation and freeing with several threads.
   */
  void TestAlignedAlloc();
  void PostAligned();

  /**
   * Tests cache aligned memory allocation and freeing with several threads.
   */
  void TestCacheAlignedAlloc();
  void PostCacheAligned();

  /**
   * Tests mixed memory allocation in detail using a single thread.
   */
  void TestMixedAllocs();

  /**
   * Tests access to allocated memory using a single thread.
   */
  void TestAccessAllocatedMemory();
  void PostAccessAllocatedMemory();

  /**
   * Stores the pointer to the allocated memory for each thread.
   */
  std::vector<void*> allocated_;
};

} // namespace test
} // namespace base
} // namespace embb

#endif  // BASE_C_TEST_ALLOC_TEST_H_
