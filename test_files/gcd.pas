fun main()
x: int;
y: int;
g: int;
a: float[12];
begin
  read(x);
  read(y);
  read(a[0]);
  g := y;
  a[0] := 0.0;
  while x > 0 do
  begin
    g := x;
    x := y - (y/x)*x;
    y := g
  end;
  write(g);
  return(0)
end
