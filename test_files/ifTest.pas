fun ifthenTest()
begin
  if 5 > 4 then
    print("Hola");
  return (0)
end

fun ifthenelseTest()
begin
  if 5 > 4 then
  skip;
  return (0)
end

fun main()
begin
  ifthenTest();
  ifthenelseTest();
  return(0)
end
