
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class TestSample {

    public static void main(String[] args) {
        inefficientJavaCode();
        efficientJavaCode();
    }

    public static void inefficientJavaCode() {
        System.out.println("Running inefficient Java code...");
        long startTime = System.currentTimeMillis();

        List<Integer> items = new ArrayList<>();
        for (int i = 0; i < 100000; i++) {
            items.add(i);
        }

        List<Integer> result = new ArrayList<>();
        // 1. Traditional for loop with get() which can be slower for some lists
        for (int i = 0; i < items.size(); i++) {
            result.add(items.get(i) * 2);
        }

        // 2. String concatenation in loop
        String s = "";
        for (int i = 0; i < 1000; i++) {
            s += i;
        }

        long endTime = System.currentTimeMillis();
        System.out.println("Inefficient Java took: " + (endTime - startTime) + "ms");
    }

    public static void efficientJavaCode() {
        System.out.println("Running efficient Java code...");
        long startTime = System.currentTimeMillis();

        List<Integer> items = IntStream.range(0, 100000).boxed().collect(Collectors.toList());

        // 1. Stream API for parallel processing and functional style
        List<Integer> result = items.stream()
                .map(x -> x * 2)
                .collect(Collectors.toList());

        // 2. StringBuilder for string concatenation
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 1000; i++) {
            sb.append(i);
        }
        String s = sb.toString();

        long endTime = System.currentTimeMillis();
        System.out.println("Efficient Java took: " + (endTime - startTime) + "ms");
    }
}
