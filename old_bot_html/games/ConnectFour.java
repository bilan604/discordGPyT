package games;
import java.util.*;


class ConnectFour {
    
    String name;
    int m;
    int n;
    ArrayList<ArrayList<String>> board;
    String colString;
    
    public ConnectFour() {
        this.name = "Connect Four";
        this.m = 6;
        this.n = 7;
        this.board = getBoard(this.m, this.n);
        this.colString = getColString();
    }

    public ConnectFour(int m, int n) {
        this.name = "Connect Four";
        this.m = m;
        this.n = n;
        this.board = getBoard(this.m, this.n);
        this.colString = getColString();
    }

    public ArrayList<ArrayList<String>> getBoard(int m, int n) {
        ArrayList<ArrayList<String>> board = new ArrayList<ArrayList<String>>();
        for (int i = 0; i < m; i++) {
            ArrayList<String> row = new ArrayList<String>();
            for (int j=0; j < n; j++) {
                row.add(" ");
            }
            board.add(row);
        }
        return board;
    }
    
    public String getColString() {
        String delimiter = "||";
        ArrayList<String> cols = new ArrayList<String>();
        for (int i = 0; i<this.n; i++) {
            cols.add(String.valueOf(i));
        }
        String colString = delimiter + String.join(delimiter, cols) + delimiter;
        return colString;
    }

    public void viewBoard() {

        String delimiter = "||";

        for (ArrayList<String> row : this.board) {
            String s = delimiter + String.join(delimiter, row) + delimiter;
            System.out.println(s);
        }
        for (int i=0; i<this.n*3 + 2; i++) {
            System.out.print("-");
        }
        System.out.print("\n");
        System.out.println(this.colString);
        
    }

    public String getBoard() {

        String delimiter = "||";

        String finalBoard = "";
        for (ArrayList<String> row : this.board) {
            ArrayList<String> newRow = new ArrayList<String>();
            for (int i=0; i<row.size(); i++) {
                newRow.add("_");
            }
            String s = delimiter + String.join(delimiter, newRow) + delimiter;
            s = "<div>" + s + "</div>\n";
            finalBoard += s;
        }
        String cut = "";
        for (int i=0; i<this.n*3 + 2; i++) {
            cut += "-";
        }
        cut = "<div>" + cut + "</div>\n";
        finalBoard += cut;
        finalBoard += "<div>" + this.colString + "</div>\n";
        return finalBoard;
        
    }

    public boolean makeValidMove(String player, int col) {
        for (int i=m-1; i>=0; i--) {
            if (this.board.get(i).get(col).equals(" ")) {
                this.board.get(i).set(col, player);
                return true;
            }
        }
        return false;
    }

    public void play(boolean player, Scanner sc) {
        String playerRepr = "X";
        if (!player) {
            playerRepr = "0";
        }

        int col = 0;
        System.out.println("Enter a column!");
        col = sc.nextInt();
        
        boolean validation = makeValidMove(playerRepr, col);
        while (!validation) {
            System.out.println("Enter a column!");
            col = sc.nextInt();
            validation = makeValidMove(playerRepr, col);
        }
        viewBoard();
    }

    public boolean over() {
        
        if (checkRightDiagonals()) {
            return true;
        }
        if (checkLeftDiagonals()) {
            return true;
        }

        for (ArrayList<String> row : this.board) {
            int c = 0;
            String prev = " ";
            for (String pos : row) {
                if (!pos.equals(" ")) {
                    if (pos.equals(prev)) {
                        c++;
                    } else {
                        c = 0;
                        if (!pos.equals(" ")) {
                            c += 1;
                        }
                        prev = pos;
                    }
                    if (c >= 4) {
                        return true;
                    }
                }
            }
        }
        for (int j=0; j<n; j++) {
            int c = 0;
            String prev = " ";
            for (int i=0; i < m; i++) {
                String pos = this.board.get(i).get(j);
                if (!pos.equals(" ")) {
                    if (pos.equals(prev)) {
                        c++;
                    } else {
                        if (!pos.equals(" ")) {
                            c = 1;
                        } else {
                            c = 0;
                        }
                        prev = pos;
                    }
                    if (c >= 4) {
                        return true;
                    }
                }
            }
        }
        return false;
    }

    public boolean checkRightDiagonals() {
        
        for (int k=0; k<this.m; k++) {
            int i=k;
            int j=0;
            int c = 0;
            String prev = " ";
            while ((i<this.m) && (j<this.n)) {
                String pos = this.board.get(i).get(j);
                if (!pos.equals(" ")) {
                    if (pos.equals(prev)) {
                        c++;
                    } else {
                        if (!pos.equals(" ")) {
                            c = 1;
                        } else {
                            c = 0;
                        }
                        prev = pos;
                    }
                    if (c >= 4) {
                        return true;
                    }
                }
                i++;
                j++;
            }
        }
        for (int k=0; k<this.n; k++) {
            int i=0;
            int j = k;
            int c = 0;
            String prev = " ";
            while ((i<this.m) && (j<this.n)) {

                String pos = this.board.get(i).get(j);
                if (!pos.equals(" ")) {
                    if (pos.equals(prev)) {
                        c++;
                    } else {
                        if (!pos.equals(" ")) {
                            c = 1;
                        } else {
                            c = 0;
                        }
                        prev = pos;
                    }
                    if (c >= 4) {
                        return true;
                    }
                }
                i++;
                j++;
            }
        }
        return false;
    }

    public boolean checkLeftDiagonals() {
        
        for (int k=0; k<this.n; k++) {
            int i=0;
            int j=k;
            int c = 0;
            String prev = " ";
            while ((i < this.m) && (-1 < j)) {
                String pos = this.board.get(i).get(j);
                if (!pos.equals(" ")) {
                    if (pos.equals(prev)) {
                        c++;
                    } else {
                        if (!pos.equals(" ")) {
                            c = 1;
                        } else {
                            c = 0;
                        }
                        prev = pos;
                    }
                    if (c >= 4) {
                        return true;
                    }
                }
                i++;
                j--;
            }
        }
        
        for (int k=0; k<this.m; k++) {
            int i = k;
            int j = this.n-1;
            int c = 0;
            String prev = " ";
            while ((i < this.m) && (-1 < j)) {
                String pos = this.board.get(i).get(j);
                if (!pos.equals(" ")) {
                    if (pos.equals(prev)) {
                        c++;
                    } else {
                        if (!pos.equals(" ")) {
                            c = 1;
                        } else {
                            c = 0;
                        }
                        prev = pos;
                    }
                    if (c >= 4) {
                        return true;
                    }
                }
                i++;
                j--;
            }
        }
        return false;

    }
}