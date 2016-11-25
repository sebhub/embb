#!/usr/bin/env python

# Copyright (c) 2016, embedded brains GmbH. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

# This script generates the "base_c/include/embb/base/c/internal/atomic/c11.h"
# header file.  It provides an implementation of the EMBB atomic operations by
# means provided by the C11 and C++11 standards.

print("""/*
 * Copyright (c) 2016, embedded brains GmbH. All rights reserved.
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

#ifndef EMBB_BASE_C_INTERNAL_ATOMIC_C11_H_
#define EMBB_BASE_C_INTERNAL_ATOMIC_C11_H_

#include <embb/base/c/internal/config.h>

#if defined EMBB_PLATFORM_ARCH_CXX11
#include <atomic>
#include <cstdint>
#elif defined EMBB_PLATFORM_ARCH_C11
#include <stdatomic.h>
#include <stddef.h>
#include <stdint.h>
#else
#error "Not available for selected C or C++ standard"
#endif

EMBB_PLATFORM_INLINE void embb_atomic_memory_barrier(void)
{
#if defined EMBB_PLATFORM_ARCH_CXX11
  std::atomic_thread_fence(std::memory_order_seq_cst);
#elif defined EMBB_PLATFORM_ARCH_C11
  atomic_thread_fence(memory_order_seq_cst);
#endif
}
""")

class Type:
	def __init__(self, name, stdName):
		self.mName = name
		self.mStdName = stdName

	def name(self):
		return self.mName

	def stdName(self):
		return self.mStdName

	def designator(self):
		return self.mName.replace(' ', '_')

# Internal typedefs

internalTypes = [
	Type("1", "uint_least8_t"),
	Type("2", "uint_least16_t"),
	Type("4", "uint_least32_t"),
	Type("8", "uint_least64_t"),
]

for t in internalTypes:
	print("typedef " + t.stdName() + " EMBB_BASE_BASIC_TYPE_SIZE_" + t.designator() + ";")
print("")

# Internal ops

class InternalOp:
	def __init__(self, embbOpFormat, stdOpFormat):
		self.mEMBBOpFormat = embbOpFormat
		self.mStdOpFormat = stdOpFormat

	def embbOp(self, d):
		return self.mEMBBOpFormat.replace("%D", d).replace("%A", "EMBB_BASE_BASIC_TYPE_SIZE_" + d)

	def stdOp(self, t, n):
		return self.mStdOpFormat.replace("%c", "(%Natomic_" + t + "*)").replace("%N", n)

internalOps = [
	InternalOp("void embb_internal__atomic_and_assign_%D(\n  %A* variable,\n  %A value\n  )",
	    "(void)%Natomic_fetch_and(%cvariable, value)"),
	InternalOp("int embb_internal__atomic_compare_and_swap_%D(\n  %A* variable,\n  %A* expected,\n  %A desired\n  )",
	    "return %Natomic_compare_exchange_strong(%cvariable, expected, desired)"),
	InternalOp("%A embb_internal__atomic_fetch_and_add_%D(\n  %A* variable,\n  %A value\n  )",
	    "return %Natomic_fetch_add(%cvariable, value)"),
	InternalOp("%A embb_internal__atomic_load_%D(\n  const %A* variable\n  )",
	    "return %Natomic_load(%cvariable)"),
	InternalOp("void embb_internal__atomic_or_assign_%D(\n  %A* variable,\n  %A value\n  )",
	    "(void)%Natomic_fetch_or(%cvariable, value)"),
	InternalOp("void embb_internal__atomic_store_%D(\n  %A* variable,\n  %A value\n  )",
	    "%Natomic_store(%cvariable, value)"),
	InternalOp("%A embb_internal__atomic_swap_%D(\n  %A* variable,\n  %A value\n  )",
	    "return %Natomic_exchange(%cvariable, value)"),
	InternalOp("void embb_internal__atomic_xor_assign_%D(\n  %A* variable,\n  %A value\n  )",
	    "(void)%Natomic_fetch_xor(%cvariable, value)"),
]

for o in internalOps:
	for t in internalTypes:
		s = "EMBB_PLATFORM_INLINE " + o.embbOp(t.designator()) + "\n"
		s += "{\n"
		s += "#if defined EMBB_PLATFORM_ARCH_CXX11\n"
		s += "  " + o.stdOp(t.stdName(), "std::") + ";\n"
		s += "#elif defined EMBB_PLATFORM_ARCH_C11\n"
		s += "  " + o.stdOp(t.stdName(), "") + ";\n"
		s += "#endif\n"
		s += "}\n"
		print(s)

# Typedefs

types = [
	Type("char", "char"),
	Type("short", "short"),
	Type("unsigned short", "ushort"),
	Type("int", "int"),
	Type("unsigned int", "uint"),
	Type("long", "long"),
	Type("unsigned long", "ulong"),
	Type("long long", "llong"),
	Type("unsigned long long", "ullong"),
	Type("intptr_t", "intptr_t"),
	Type("uintptr_t", "uintptr_t"),
	Type("size_t", "size_t"),
	Type("ptrdiff_t", "ptrdiff_t"),
	Type("uintmax_t", "uintmax_t")
]

print("#if defined EMBB_PLATFORM_ARCH_CXX11\n")
for t in types:
	print("typedef std::atomic_" + t.stdName() + " embb_atomic_" + t.designator() + ";")
print("\n#elif defined EMBB_PLATFORM_ARCH_C11\n")
for t in types:
	print("typedef atomic_" + t.stdName() + " embb_atomic_" + t.designator() + ";")
print("\n#endif\n")

# Ops

class Op:
	def __init__(self, embbOpFormat, stdOpFormat):
		self.mEMBBOpFormat = embbOpFormat
		self.mStdOpFormat = stdOpFormat

	def embbOp(self, t, d):
		return self.mEMBBOpFormat.replace("%T", t).replace("%D", d).replace("%A", "embb_atomic_" + d)

	def stdOp(self, n):
		return self.mStdOpFormat.replace("%N", n)

ops = [
	Op("void embb_atomic_and_assign_%D(\n  %A* variable,\n  %T value\n  )",
	    "(void)%Natomic_fetch_and(variable, value)"),
	Op("int embb_atomic_compare_and_swap_%D(\n  %A* variable,\n  %T* expected,\n  %T desired\n  )",
	    "return %Natomic_compare_exchange_strong(variable, expected, desired)"),
	Op("void embb_atomic_destroy_%D(\n  %A* variable\n  )",
	    "(void)variable"),
	Op("%T embb_atomic_fetch_and_add_%D(\n  %A* variable,\n  %T value\n  )",
	    "return %Natomic_fetch_add(variable, value)"),
	Op("void embb_atomic_init_%D(\n  %A* variable,\n  %T value\n  )",
	    "%Natomic_init(variable, value)"),
	Op("%T embb_atomic_load_%D(\n  const %A* variable\n  )",
	    "return %Natomic_load(variable)"),
	Op("void embb_atomic_or_assign_%D(\n  %A* variable,\n  %T value\n  )",
	    "(void)%Natomic_fetch_or(variable, value)"),
	Op("void embb_atomic_store_%D(\n  %A* variable,\n  %T value\n  )",
	    "%Natomic_store(variable, value)"),
	Op("%T embb_atomic_swap_%D(\n  %A* variable,\n  %T value\n  )",
	    "return %Natomic_exchange(variable, value)"),
	Op("void embb_atomic_xor_assign_%D(\n  %A* variable,\n  %T value\n  )",
	    "(void)%Natomic_fetch_xor(variable, value)"),
]

for o in ops:
	for t in types:
		s = "EMBB_PLATFORM_INLINE " + o.embbOp(t.name(), t.designator()) + "\n"
		s += "{\n"
		s += "#if defined EMBB_PLATFORM_ARCH_CXX11\n"
		s += "  " + o.stdOp("std::") + ";\n"
		s += "#elif defined EMBB_PLATFORM_ARCH_C11\n"
		s += "  " + o.stdOp("") + ";\n"
		s += "#endif\n"
		s += "}\n"
		print(s)

print("#endif //EMBB_BASE_C_INTERNAL_ATOMIC_C11_H_")