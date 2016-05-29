fun foo()
begin
  return (0)
end

fun main()
x: int;
y: int;
g: int;
a: int;
i: int;
begin
  read(x);
  read(y);
  g := y;
  while x > 0 do
  begin
    g := x;
    x := y - (y/x)*x;
    x := foo() + 2;
    y := g
  end;
  write(g);
  return(0)
end
