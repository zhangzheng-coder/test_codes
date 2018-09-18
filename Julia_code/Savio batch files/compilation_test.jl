using BuildExecutable
using Base.Test
using Compat
build_executable("test_exec", "test_code.jl", "exec_folder", "native")