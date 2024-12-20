import { boot } from "quasar/wrappers";

import * as echarts from "echarts/core";
import { SVGRenderer } from "echarts/renderers";
import { PieChart, LineChart, BarChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
} from "echarts/components";
import { UniversalTransition } from "echarts/features";

export default boot(() => {
  echarts.use([
    SVGRenderer,
    TooltipComponent,
    LegendComponent,
    TitleComponent,
    GridComponent,
    UniversalTransition,
    PieChart,
    LineChart,
    BarChart,
  ]);
});
