#  Copyright (c) 2022 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import numpy as np
import unittest
from op_test import OpTest, skip_check_grad_ci
import paddle

paddle.enable_static()


class ElementwiseMulOp(OpTest):
    def set_sdaa(self):
        self.__class__.use_custom_device = True
        self.place = paddle.CustomPlace("sdaa", 0)

    def setUp(self):
        self.set_sdaa()
        self.op_type = "elementwise_mul"
        self.python_api = paddle.multiply
        self.init_dtype()
        self.init_input_output()
        self.init_axis()

        self.inputs = {
            "X": OpTest.np_dtype_to_base_dtype(self.x),
            "Y": OpTest.np_dtype_to_base_dtype(self.y),
        }
        self.outputs = {"Out": self.out}
        self.attrs = {"axis": self.axis}

    def test_check_output(self):
        self.check_output_with_place(self.place)

    def test_check_grad_normal(self):
        if (
            self.dtype == np.bool_
            or self.dtype == np.uint8
            or self.dtype == np.int8
            or self.dtype == np.int16
            or self.dtype == np.int32
            or self.dtype == np.int64
        ):
            return
        self.check_grad_with_place(self.place, ["X", "Y"], "Out")

    def test_check_grad_ingore_x(self):
        if (
            self.dtype == np.bool_
            or self.dtype == np.uint8
            or self.dtype == np.int8
            or self.dtype == np.int16
            or self.dtype == np.int32
            or self.dtype == np.int64
        ):
            return
        self.check_grad_with_place(
            self.place,
            ["Y"],
            "Out",
            no_grad_set=set("X"),
        )

    def test_check_grad_ingore_y(self):
        if (
            self.dtype == np.bool_
            or self.dtype == np.uint8
            or self.dtype == np.int8
            or self.dtype == np.int16
            or self.dtype == np.int32
            or self.dtype == np.int64
        ):
            return
        self.check_grad_with_place(
            self.place,
            ["X"],
            "Out",
            no_grad_set=set("Y"),
        )

    def init_input_output(self):
        self.x = np.random.uniform(0.1, 1, [13, 17]).astype(self.dtype)
        self.y = np.random.uniform(0.1, 1, [13, 17]).astype(self.dtype)
        self.out = np.multiply(self.x, self.y)

    def init_dtype(self):
        self.dtype = np.float32

    def init_axis(self):
        self.axis = -1


@skip_check_grad_ci(reason="[skip shape check] Use y_shape(1) to test broadcast.")
class TestElementwiseMulOp_scalar(ElementwiseMulOp):
    def init_input_output(self):
        self.x = np.random.rand(10, 3, 4).astype(self.dtype)
        self.y = np.random.rand(1).astype(self.dtype)
        self.out = np.multiply(self.x, self.y)


class TestElementwiseMulOp_Vector(ElementwiseMulOp):
    def init_input_output(self):
        self.x = np.random.random((100,)).astype(self.dtype)
        self.y = np.random.random((100,)).astype(self.dtype)
        self.out = np.multiply(self.x, self.y)


class TestElementwiseMulOp_Nd_1(ElementwiseMulOp):
    def init_input_output(self):
        self.x = np.random.uniform(0.1, 1, [3, 4, 5, 6, 2]).astype(self.dtype)
        self.y = np.random.uniform(0.1, 1, [3, 4, 5, 6, 2]).astype(self.dtype)
        self.out = np.multiply(self.x, self.y)


class TestElementwiseMulOp_Nd_2(ElementwiseMulOp):
    def init_input_output(self):
        self.x = np.random.uniform(0.1, 1, [3, 2, 5, 2, 4, 3]).astype(self.dtype)
        self.y = np.random.uniform(0.1, 1, [3, 2, 5, 2, 4, 3]).astype(self.dtype)
        self.out = np.multiply(self.x, self.y)


class TestElementwiseMulOp_broadcast_0(ElementwiseMulOp):
    def init_input_output(self):
        self.x = np.random.rand(100, 2, 3).astype(self.dtype)
        self.y = np.random.rand(100).astype(self.dtype)
        self.out = np.multiply(self.x, self.y.reshape(100, 1, 1))

    def init_axis(self):
        self.axis = 0


class TestElementwiseMulOp_broadcast_1(ElementwiseMulOp):
    def init_input_output(self):
        self.x = np.random.rand(2, 100, 3).astype(self.dtype)
        self.y = np.random.rand(100).astype(self.dtype)
        self.out = np.multiply(self.x, self.y.reshape(1, 100, 1))

    def init_axis(self):
        self.axis = 1


class TestElementwiseMulOp_broadcast_2(ElementwiseMulOp):
    def init_input_output(self):
        self.x = np.random.rand(2, 3, 100).astype(self.dtype)
        self.y = np.random.rand(100).astype(self.dtype)
        self.out = np.multiply(self.x, self.y.reshape(1, 1, 100))


class TestElementwiseMulOp_broadcast_3(ElementwiseMulOp):
    def init_input_output(self):
        self.x = np.random.rand(2, 10, 12, 3).astype(self.dtype)
        self.y = np.random.rand(10, 12).astype(self.dtype)
        self.out = np.multiply(self.x, self.y.reshape(1, 10, 12, 1))

    def init_axis(self):
        self.axis = 1


class TestElementwiseMulOp_broadcast_4(ElementwiseMulOp):
    def init_input_output(self):
        self.x = np.random.rand(10, 2, 11).astype(self.dtype)
        self.y = np.random.rand(10, 1, 11).astype(self.dtype)
        self.out = np.multiply(self.x, self.y)


class TestElementwiseMulOp_broadcast_5(ElementwiseMulOp):
    def init_input_output(self):
        self.x = np.random.rand(10, 4, 2, 3).astype(self.dtype)
        self.y = np.random.rand(10, 4, 1, 3).astype(self.dtype)
        self.out = np.multiply(self.x, self.y)


class TestElementwiseMulOp_broadcast_6(ElementwiseMulOp):
    def init_input_output(self):
        self.x = np.random.rand(3, 4, 2, 3, 4).astype(self.dtype)
        self.y = np.random.rand(3, 4, 1, 3, 4).astype(self.dtype)
        self.out = np.multiply(self.x, self.y)


class TestElementwiseMulOpBool(ElementwiseMulOp):
    def init_dtype(self):
        self.dtype = np.bool_


class TestElementwiseMulOpUint8(ElementwiseMulOp):
    def init_dtype(self):
        self.dtype = np.uint8

    def init_input_output(self):
        self.x = np.random.randint(2, 10, [13, 17]).astype(self.dtype)
        self.y = np.random.randint(2, 10, [13, 17]).astype(self.dtype)
        self.out = np.multiply(self.x, self.y)


class TestElementwiseMulOpInt8(ElementwiseMulOp):
    def init_dtype(self):
        self.dtype = np.int8

    def init_input_output(self):
        self.x = np.random.randint(2, 10, [13, 17]).astype(self.dtype)
        self.y = np.random.randint(2, 10, [13, 17]).astype(self.dtype)
        self.out = np.multiply(self.x, self.y)


class TestElementwiseMulOpInt16(ElementwiseMulOp):
    def init_dtype(self):
        self.dtype = np.int16

    def init_input_output(self):
        self.x = np.random.randint(2, 10, [13, 17]).astype(self.dtype)
        self.y = np.random.randint(2, 10, [13, 17]).astype(self.dtype)
        self.out = np.multiply(self.x, self.y)


class TestElementwiseMulOpInt32(ElementwiseMulOp):
    def init_dtype(self):
        self.dtype = np.int32

    def init_input_output(self):
        self.x = np.random.randint(2, 10, [13, 17]).astype(self.dtype)
        self.y = np.random.randint(2, 10, [13, 17]).astype(self.dtype)
        self.out = np.multiply(self.x, self.y)


class TestElementwiseMulOpInt64(ElementwiseMulOp):
    def init_dtype(self):
        self.dtype = np.int64

    def init_input_output(self):
        self.x = np.random.randint(2, 10, [13, 17]).astype(self.dtype)
        self.y = np.random.randint(2, 10, [13, 17]).astype(self.dtype)
        self.out = np.multiply(self.x, self.y)


class TestElementwiseMulOpDouble(ElementwiseMulOp):
    def init_dtype(self):
        self.dtype = np.double


class TestElementwiseMulOpFp16(ElementwiseMulOp):
    def init_dtype(self):
        self.dtype = np.float16


class TestElementwiseMulOp_commonuse_1(ElementwiseMulOp):
    def init_input_output(self):
        self.x = np.random.rand(2, 3, 100).astype(self.dtype)
        self.y = np.random.rand(1, 1, 100).astype(self.dtype)
        self.out = np.multiply(self.x, self.y)


class TestElementwiseMulOp_commonuse_2(ElementwiseMulOp):
    def init_input_output(self):
        self.x = np.random.rand(10, 3, 1, 5).astype(self.dtype)
        self.y = np.random.rand(10, 1, 4, 5).astype(self.dtype)
        self.out = np.multiply(self.x, self.y)


class TestElementwiseMulOp_commonuse_3(ElementwiseMulOp):
    def init_input_output(self):
        self.x = np.random.rand(20, 3, 4, 5, 1).astype(self.dtype)
        self.y = np.random.rand(20, 1, 4, 1, 2).astype(self.dtype)
        self.out = np.multiply(self.x, self.y)


class TestElementwiseMulOp_xsize_lessthan_ysize(ElementwiseMulOp):
    def init_input_output(self):
        self.x = np.random.rand(10, 10).astype(self.dtype)
        self.y = np.random.rand(2, 2, 10, 10).astype(self.dtype)
        self.out = np.multiply(self.x.reshape(1, 1, 10, 10), self.y)

    def init_axis(self):
        self.axis = 2


class TestElementwiseMulApi_broadcast_dim_1(unittest.TestCase):

    paddle.disable_static()
    paddle.set_device("sdaa")
    np_x = np.random.uniform(0.1, 1.0, [768]).astype("float32")
    np_y = np.random.uniform(0.1, 1.0, [1, 1]).astype("float32")

    x = paddle.to_tensor(np_x, stop_gradient=False)
    y = paddle.to_tensor(np_y, stop_gradient=False)
    z = paddle.multiply(x, y)
    z.backward()

    paddle.set_device("cpu")
    xc = x._to("cpu")
    yc = y._to("cpu")
    zc = paddle.multiply(xc, yc)
    zc.backward()

    np.testing.assert_allclose(z, zc)
    np.testing.assert_allclose(x.grad, xc.grad)
    np.testing.assert_allclose(y.grad, yc.grad)
    paddle.enable_static()


if __name__ == "__main__":
    unittest.main()
