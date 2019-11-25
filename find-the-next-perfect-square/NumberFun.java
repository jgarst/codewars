/*
 *  This is a simple Java program
 *
 */

class NumberFun {
  public static void main(String args[]) {
    System.out.println(findNextSquare(1));
    System.out.println(findNextSquare(2));
    System.out.println(findNextSquare(3));
    System.out.println(findNextSquare(4));
  }

  public static long findNextSquare(long sq) {
    double sqrt = Math.sqrt(sq);
    if(sqrt == (long) sqrt) {
      return (long) Math.pow(sqrt + 1, 2);
    } else {
      return -1;
    }
  }
}


