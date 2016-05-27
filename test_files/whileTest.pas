fun whileUnary(i:int)
begin
  while not i < 2 do
    skip;
  return (0)
end

fun whileBin(i:int)
begin
  while i < 2 do
    begin
      i := 1;
      i := 2
    end;
  return (0)
end

fun main()
begin
  whileBin(0);
  return (0)
end
