package test;

import com.csvreader.CsvReader;
import com.csvreader.CsvWriter;

import java.io.IOException;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.List;

public class Demo01 {
    public static void main(String[] args) {
        System.out.println("hello world");
        String filePath = "F:\\workSpace\\py\\py量化\\abtc\\2_abtc_轮动\\abtc_轮动_改进.csv";
//        String filePath = "F:\\workSpace\\py\\py量化\\abtc\\2_abtc_轮动\\abtc_轮动.csv";
        List<String[]> csvContent = readCsvFile(filePath);

        LinkedHashMap<String, Integer> headerIndexMap = new LinkedHashMap<>();
        String[] headerRow = csvContent.get(0);
        for (int i = 0; i < headerRow.length; i++) {
            headerIndexMap.put(headerRow[i],i);
        }

        for (int i = 1; i < csvContent.size(); i++) {

            double strategy_pct_adjust = Double.parseDouble(csvContent.get(i)[headerIndexMap.get("strategy_pct_adjust")]);

            double total_capital_lastrow = 0.0;//第一行表头的默认值
            if (i - 1 != 0) { //第一行表头的情况排除  使用默认值
                total_capital_lastrow = Double.parseDouble(csvContent.get(i - 1)[headerIndexMap.get("total_capital")]);
            }

            double normal_capital = Double.parseDouble(csvContent.get(i)[headerIndexMap.get("normal_capital")]);

            double total_capital = total_capital_lastrow * (1 + strategy_pct_adjust) + normal_capital;

            csvContent.get(i)[headerIndexMap.get("total_capital")] = String.valueOf(total_capital);

        }


        for (int row = 0; row < csvContent.size(); row++) {
            String[] rowArr = csvContent.get(row);
            System.out.println(Arrays.toString(rowArr));
        }

        write(filePath, csvContent);

    }

    /**
     * 读取 csv 文件
     */
    public static List<String[]> readCsvFile(String readCsvFilePath) {
        // 缓存读取的数据
        List<String[]> content = new ArrayList<>();

        try {
            // 创建 CSV Reader 对象, 参数说明（读取的文件路径，分隔符，编码格式)
            CsvReader csvReader = new CsvReader(readCsvFilePath, ',', Charset.forName("GBK"));
            // 跳过表头
//            csvReader.readHeaders();

            // 读取除表头外的内容
            while (csvReader.readRecord()) {
                // 读取一整行
                String line = csvReader.getRawRecord();
//                System.out.println(line);

                content.add(csvReader.getValues());
            }
            csvReader.close();


        } catch (Exception e) {
            e.printStackTrace();
        }
        return content;
    }


    public static void write(String filePath, List<String[]> content) {

//        String filePath = "/Users/dddd/test.csv";

        try {
            // 创建CSV写对象
            CsvWriter csvWriter = new CsvWriter(filePath, ',', Charset.forName("GBK"));
            //CsvWriter csvWriter = new CsvWriter(filePath);

            for (int i = 0; i < content.size(); i++) {
                csvWriter.writeRecord(content.get(i));
            }
            csvWriter.close();

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}
