fun hanoi(n:int, src:int, dest:int, spare:int)
begin
  if n == 1 then
    begin
      print("mueva ");
      write(src);
      print(" a ");
      write(dest);
      print("\n")
    end
  else
    begin
      hanoi(n-1, src, spare, dest);
      hanoi(1, src, dest, spare);
      hanoi(n-1, spare, dest, src)
    end
end

fun main()
n:int;
begin
  print("Las Torres de Hanoi.\n");
  print("Entre el número de discos: ");
  read(n);
  hanoi(n, 1, 3, 2)
end
