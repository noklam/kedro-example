# Copyright 2021 QuantumBlack Visual Analytics Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND
# NONINFRINGEMENT. IN NO EVENT WILL THE LICENSOR OR OTHER CONTRIBUTORS
# BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# The QuantumBlack Visual Analytics Limited ("QuantumBlack") name and logo
# (either separately or in combination, "QuantumBlack Trademarks") are
# trademarks of QuantumBlack. The License does not grant you any right or
# license to the QuantumBlack Trademarks. You may not use the QuantumBlack
# Trademarks or any confusingly similar mark as a trademark for your product,
# or use the QuantumBlack Trademarks in any other manner that might cause
# confusion in the marketplace, including but not limited to in advertising,
# on websites, or on software.
#
# See the License for the specific language governing permissions and
# limitations under the License.

"""Example code for the nodes in the example pipeline. This code is meant
just for illustrating basic Kedro features.

Delete this when you start working on your own Kedro project.
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import node1_func, node2_func, add

def defrost(x):
    print('defrost')
    return 'defrost'

def grill(x):
    print('grill')
    return 'grill'


cook_pipeline = Pipeline(
    [
        node(defrost, "frozen_meat", "meat", name="defrost_node"),
        node(grill, "meat", "grilled_meat"),
    ]
)

cook_breakfast_pipeline = pipeline(
    cook_pipeline,
    inputs={"frozen_meat": "frozen_meat"},  # inputs stay the same, don't namespace
    # outputs={"grilled_meat": "breakfast_food"},
    namespace="breakfast",
)
cook_lunch_pipeline = pipeline(
    cook_pipeline,
    inputs={"frozen_meat": "frozen_meat"},  # inputs stay the same, don't namespace
    # outputs={"grilled_meat": "lunch_food"},
    namespace="lunch",
)

final_pipeline = (
    cook_breakfast_pipeline
    + cook_lunch_pipeline
)

def create_pipeline():
    return final_pipeline
    # node1 = node(func=node1_func, inputs="a", outputs="b")
    # node2 = node(func=node2_func, inputs="c", outputs="d")
    # node3 = node(func=add, inputs=["b", "d"], outputs="sum")
    # return Pipeline([node1, node2, node3])