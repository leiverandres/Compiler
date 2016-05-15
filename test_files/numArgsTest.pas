fun test(arg1:int, arg2:int)
begin
  skip
end

fun nestedTest(arg1:int, arg2:int)
fun nest1(arg3:int, arg4:int)
begin
  arg1 := 2
end;
begin
  skip
end

fun main()
begin
  test(1, 2)
end
