fun assignTest()
i:int;
j:float[122];
k:int;
h:float;
begin
  i := 2;
  j[13] := 1.0 + 3.0;
  k := i + 2;
  h := j[5] + 2.0
end

fun main()
begin
  assignTest()
end
