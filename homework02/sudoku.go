package main

import (
	"fmt"
	"io/ioutil"
	"math/rand"
	"path/filepath"
	"sort"
	"time"
)

func readSudoku(filename string) ([][]byte, error) {
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		return nil, err
	}
	grid := group(filter(data), 9)
	return grid, nil
}

func filter(values []byte) []byte {
	filtered_values := make([]byte, 0)
	for _, v := range values {
		if (v >= '1' && v <= '9') || v == '.' {
			filtered_values = append(filtered_values, v)
		}
	}
	return filtered_values
}

func display(grid [][]byte) {
	for i := 0; i < len(grid); i++ {
		for j := 0; j < len(grid); j++ {
			fmt.Print(string(grid[i][j]))
		}
		fmt.Println()
	}
}

func group(values []byte, n int) [][]byte {
	var groups [][]byte
	for i := 0; i < len(values); i += n {
		groups = append(groups, (values[i : i+n]))
	}
	return groups
}

func getRow(grid [][]byte, row int) []byte {
	return grid[row]
}

func getCol(grid [][]byte, col int) []byte {
	var column []byte
	for i := 0; i < len(grid); i++ {
		column = append(column, grid[i][col])
	}
	return column
}

func getBlock(grid [][]byte, row int, col int) []byte {
	var r, c int
	var block []byte
	r = 3 * (row / 3)
	c = 3 * (col / 3)
	for i := 0; i < 3; i++ {
		for j := 0; j < 3; j++ {
			block = append(block, grid[r+i][c+j])
		}
	}
	return block
}

func findEmptyPosition(grid [][]byte) (int, int) {
	for row := 0; row < len(grid); row++ {
		for col := 0; col < len(grid); col++ {
			if grid[row][col] == '.' {
				return row, col
			}
		}

	}
	return -1, -1
}

func contains(values []byte, search byte) bool {
	for _, v := range values {
		if v == search {
			return true
		}
	}
	return false
}

func findPossibleValues(grid [][]byte, row int, col int) []byte {
	var Values []byte
	a := []byte("123456789")
	b := getRow(grid, row)
	c := getCol(grid, col)
	d := getBlock(grid, row, col)
	for i := 0; i < 9; i++ {
		flag := 0
		for j := 0; j < 9; j++ {
			if (a[i] == b[j]) || (a[i] == c[j]) || (a[i] == d[j]) {
				flag = 1
			}
		}
		if flag == 0 {
			Values = append(Values, a[i])
		}
	}
	return Values
}

func solve(grid [][]byte) ([][]byte, bool) {
	var none [][]byte
	row, col := findEmptyPosition(grid)
	if col == -1 {
		return grid, true
	}
	for _, value := range findPossibleValues(grid, row, col) {
		grid[row][col] = value
		solution, boolean := solve(grid)
		if boolean == true {
			return solution, boolean
		}
	}
	grid[row][col] = '.'
	return none, false
}

func checkSolution(grid [][]byte) bool {
	var int_val []int
	set := []byte("123456789")
	for str := 0; str < len(grid); str++ {
		int_val = []int{}
		values := getRow(grid, str)
		for i := 0; i < len(values); i++ {
			int_val = append(int_val, int(values[i]))
		}
		sort.Ints(int_val)
		//fmt.Println(int_val)
		//fmt.Println(set)
		for i := 0; i < len(int_val); i++ {
			if int_val[i] != int(set[i]) {
				return false
			}

		}
	}

	for column := 0; column < len(grid); column++ {
		int_val = []int{}
		values := getCol(grid, column)
		for i := 0; i < len(values); i++ {
			int_val = append(int_val, int(values[i]))
		}
		sort.Ints(int_val)
		for i := 0; i < len(int_val); i++ {
			if int_val[i] != int(set[i]) {
				return false
			}

		}

	}
	for _, str := range []int{0, 3, 6} {
		for _, column := range []int{0, 3, 6} {
			int_val = []int{}
			values := getBlock(grid, str, column)
			for i := 0; i < len(values); i++ {
				int_val = append(int_val, int(values[i]))
			}
			sort.Ints(int_val)
			for i := 0; i < len(int_val); i++ {
				if int_val[i] != int(set[i]) {
					return false
				}

			}
		}
	}
	return true
}

func generateSudoku(N int) [][]byte {
	var sudoku [][]byte
	a := []byte(".........")
	for i := 0; i < 9; i++ {
		sudoku = append(sudoku, a)
	}
	sudoku, _ = solve(sudoku)
	if N > 81 {
		N = 0
	} else {
		N = 81 - N
	}
	rand.Seed(time.Now().UnixNano())
	for N > 0 {
		row := rand.Intn(8)
		col := rand.Intn(8)
		if sudoku[row][col] != '.' {
			sudoku[row][col] = '.'
		}
		N -= 1
	}
	return sudoku
}

func main() {
	puzzles, err := filepath.Glob("puzzle*.txt")
	if err != nil {
		fmt.Printf("Could not find any puzzles")
		return
	}
	for _, fname := range puzzles {
		go func(fname string) {
			grid, _ := readSudoku(fname)
			solution, _ := solve(grid)
			checkSolution(solution)
			fmt.Println("Solution for", fname)
			display(solution)
		}(fname)
	}
	var input string
	fmt.Scanln(&input)
}
