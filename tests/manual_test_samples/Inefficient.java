
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class Inefficient {

    public static void main(String[] args) {
        System.out.println("Running inefficient Java code...");
        long startTime = System.currentTimeMillis();

        // 1. Inefficient loop iteration (Pattern: manual for loop)
        List<Integer> list = new ArrayList<>();
        for (int i = 0; i < 50000; i++) {
            list.add(i);
        }

        List<Integer> result = new ArrayList<>();
        for (int i = 0; i < list.size(); i++) {
            // Inefficient: Repeatedly calling .get(i) on list (O(n^2) for LinkedList, adds
            // overhead for ArrayList)
            Integer val = list.get(i);

            // Inefficient: Manual loop logic instead of Stream/parallelStream
            if (val % 2 == 0) {
                result.add(val * 2);
            }
        }

        // 2. String Concatenation in Loop (Pattern: += string)
        String s = "";
        for (int i = 0; i < 2000; i++) {
            // Inefficient: Creates a new StringBuilder and String object each iteration
            s += "number" + i;
        }

        // 3. Excessive Auto-boxing (Pattern: Integer vs int)
        // Metric: Creates unnecessary objects, GC pressure
        Integer sum = 0; // Boxing
        for (int i = 0; i < 100000; i++) {
            sum += i; // Unboxing and re-boxing every iteration
        }

        // 4. Inefficient wrapper class usage
        // Using Boolean instead of boolean
        Boolean flag = Boolean.TRUE;
        if (flag) {
        }

        // 5. Unbuffered I/O (Simulated)
        // Would be System.out.print inside loop without buffer

        long endTime = System.currentTimeMillis();
        System.out.println("Inefficient Java finished in " + (endTime - startTime) + "ms");
    }
}
