# Gauss-elimination

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/9aa197ad25294a3cbd491ded8311e75e)](https://www.codacy.com/app/Drapegnik/Gauss-elimination?utm_source=github.com&utm_medium=referral&utm_content=Drapegnik/Gauss-elimination&utm_campaign=badger)
[![Code Climate](https://codeclimate.com/github/Drapegnik/Gauss-elimination/badges/gpa.svg)](https://codeclimate.com/github/Drapegnik/Gauss-elimination)
[![Issue Count](https://codeclimate.com/github/Drapegnik/Gauss-elimination/badges/issue_count.svg)](https://codeclimate.com/github/Drapegnik/Gauss-elimination)

:rocket: multithread solving linear system with Gauss-Jordan elimination

**requirements**:

- [python](https://www.python.org/)
- use `pip install requirements.txt` for [numpy](http://www.numpy.org/) &
  [mpi4py](http://pythonhosted.org/mpi4py/)

**run**:

```
$ bash run.sh {matrix_dimension} {values_range} {number_of_procces}
```

**or**

```
$ ./run.sh {matrix_dimension} {values_range} {number_of_procces}
```

**for example**: `$ bash run.sh 3 10 3`:

- generate random matrix `A` with size `(3,3)` and vector `b`
- for `A` find inversed matrix `A_inv` using `3` process
- solve equation like `x = A_inv * b`
- write ouputs, count time

<img src="http://res.cloudinary.com/dzsjwgjii/image/upload/v1479125055/lab2.png" width=900px/>

**Notes**

- for direct input use `input.txt`
- inverse matrix and vector `x` stored in `output.txt`
