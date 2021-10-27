import React, { useState, useEffect } from "react";
import { scaleLinear } from "d3-scale";
import { range } from "d3-array";
import { format } from "d3-format";
import {
  ReferenceArea,
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  ReferenceLine,
  Tooltip,
  ResponsiveContainer,
  ZAxis,
} from "recharts";

export const RechartsHistogram = ({ inpdata, axis }) => {
  const [isHistogram, setIsHistogram] = useState(false);
  const [isScatter, setIsScatter] = useState(false);

  const isColourBar = 1;

  const countMax = inpdata.hist_data.reduce((a, b) =>
    a.counts > b.counts ? a : b
  ).counts;
  const countMin = inpdata.hist_data.reduce((a, b) =>
    a.counts < b.counts ? a : b
  ).counts;

  const AXIS_SCALE = 0.05;
  const NUM_TICKS = 6;
  const COLOUR_CELLS = 10;

  const diffRange_x =
    Math.abs(inpdata.minmax_x[1] - inpdata.minmax_x[0]) * AXIS_SCALE;
  const diffRange_y =
    Math.abs(inpdata.minmax_y[1] - inpdata.minmax_y[0]) * AXIS_SCALE;
  const plot_min_x = Math.floor((inpdata.minmax_x[0] - diffRange_x) * 10) / 10;
  const plot_max_x = Math.ceil((inpdata.minmax_x[1] + diffRange_x) * 10) / 10;
  const plot_min_y = Math.floor((inpdata.minmax_y[0] - diffRange_y) * 10) / 10;
  const plot_max_y = Math.ceil((inpdata.minmax_y[1] + diffRange_y) * 10) / 10;

  const createTicks = (min, max, num_ticks) => {
    const tickSteps = Math.abs(max - min) / num_ticks;
    const axisRange = range(min, max * 1.01, tickSteps);
    return axisRange;
  };

  const ticks_x = createTicks(plot_min_x, plot_max_x, NUM_TICKS);
  const ticks_y = createTicks(plot_min_y, plot_max_y, NUM_TICKS);

  const col = scaleLinear(
    [Math.log10(countMin), Math.log10(countMax)],
    ["purple", "yellow"]
  );

  const colourRange = range(
    Math.log10(countMin),
    Math.log10(countMax) * 1.001,
    (Math.log10(countMax) - Math.log10(countMin)) / COLOUR_CELLS
  );

  const formatAxis = (value) => {
    if (Math.abs(value) > 1e3) {
      return format(".1e")(value);
    }
    return format(".1f")(value);
  };

  const CustomTooltip = ({ active, payload, label }) => {
    // console.log(payload);
    if (active && payload && payload.length) {
      const divStyle = {
        margin: "0",
        lineHeight: "5px",
        border: "1px solid #f5f5f5",
        backgroundColor: "rgba(255, 255, 255, 0.8)",
        paddingBottom: "0%",
      };

      const pStyle = {
        paddingTop: "calc(0.3rem + 1px)",
        paddingBottom: "calc(0.3rem + 1px)",
        margin: "0",
        fontSize: "10px",
      };

      return (
        <div style={divStyle}>
          {payload[2] && (
            <p style={ pStyle }>{`Counts : ${format(".0f")(
              payload[2].value
            )}`}</p>
          )}

          {inpdata.minmax_x[2] ? (
            <p style={ pStyle }>{`${
              payload[0].value <= inpdata.minmax_x[0] + inpdata.sides[0] / 2
                ? `null`
                : inpdata.log_check_x
                ? `log[${axis[0]}]`
                : axis[0]
            } : ${format(".4f")(payload[0].value)}`}</p>
          ) : (
            <p style={ pStyle }>{`${
              inpdata.log_check_x ? `log[${axis[0]}]` : axis[0]
            } : ${format(".4f")(payload[0].value)}`}</p>
          )}

          <p style={ pStyle }>{`${
            inpdata.log_check_y ? `log[${axis[1]}]` : axis[1]
          } : ${format(".4f")(payload[1].value)}`}</p>
        </div>
      );
    }

    return null;
  };

  useEffect(() => {
    console.log("this");
    // console.log(inpdata);
    // console.log(
    //   inpdata.hist_data.reduce((a, b) => (a.counts < b.counts ? a : b)).counts
    // );
  }, []);

  useEffect(() => {
    if (inpdata.hist_data) {
      // console.log(inpdata);
      setIsHistogram(true);
    } else {
      console.log("reached here somehow");
      setIsHistogram(false);
    }
    if (inpdata.scatter_data) {
      setIsScatter(true);
    } else {
      setIsScatter(false);
    }
  }, [inpdata]);

  return (
    <ResponsiveContainer width="85%" aspect={1} minWidth={500}>
      <ScatterChart
        width={500}
        height={500}
        margin={{
          top: 30,
          right: 130,
          bottom: 130,
          left: 80,
        }}
      >
        {/* <CartesianGrid strokeDasharray="3 3" /> */}
        <XAxis
          dataKey={"x"}
          label={{
            value: inpdata.log_check_x ? `log[${axis[0]}]` : axis[0],
            position: "insideBottomRight",
            dx: 5,
            dy: 20,
            stroke: "#9E9E9E",
            fontSize: 15,
          }}
          type="number"
          ticks={inpdata.minmax_x[2] ? ticks_x.slice(1) : ticks_x}
          tick={{ fontSize: 13, transform: "translate(0, 3)" }}
          tickFormatter={formatAxis}
          domain={[plot_min_x, plot_max_x]}
        />
        <YAxis
          dataKey={"y"}
          label={{
            value: inpdata.log_check_y ? `log[${axis[1]}]` : axis[1],
            position: "insideTopLeft",
            angle: -90,
            dx: -15,
            dy: 0,
            stroke: "#9E9E9E",
            style: { textAnchor: "end" },
            fontSize: 15,
          }}
          type="number"
          ticks={inpdata.minmax_y[2] ? ticks_y.slice(1) : ticks_y}
          tick={{ fontSize: 13, transform: "translate(-3, 0)" }}
          tickFormatter={formatAxis}
          domain={[plot_min_y, plot_max_y]}
        />
        <ZAxis zAxisId="invis-z" dataKey="counts" range={[100, 100]} />
        <ZAxis zAxisId="standard" dataKey="counts" range={[15, 15]} />
        <Tooltip cursor={false} content={<CustomTooltip />} />

        {inpdata.minmax_x[2] && (
          <ReferenceLine
            segment={[
              { x: inpdata.minmax_x[0] + inpdata.sides[0] / 2, y: plot_max_y },
              { x: inpdata.minmax_x[0] + inpdata.sides[0] / 2, y: plot_min_y },
            ]}
            stroke="#cacaca"
            strokeOpacity={0.7}
            strokeDasharray="4 6"
            strokeWidth={2}
            label={{
              value: "NULL",
              angle: -90,
              position: "insideBottomLeft",
              stroke: "#cacaca",
              opacity: 0.9,
              dx: -15,
              fontSize: 10,
            }}
            ifOverflow="visible"
          />
        )}

        {inpdata.minmax_y[2] && (
          <ReferenceLine
            segment={[
              { x: plot_max_x, y: inpdata.minmax_y[0] + inpdata.sides[1] / 2 },
              { x: plot_min_x, y: inpdata.minmax_y[0] + inpdata.sides[1] / 2 },
            ]}
            stroke="#cacaca"
            strokeOpacity={0.7}
            strokeDasharray="4 6"
            strokeWidth={2}
            label={{
              value: "NULL",
              position: "insideBottomLeft",
              stroke: "#cacaca",
              opacity: 0.9,
              dy: 0,
              fontSize: 10,
            }}
            ifOverflow="visible"
          />
        )}

        {isColourBar && (
          <ReferenceArea
            key={`extra`}
            x1={
              plot_max_x +
              6 * (inpdata.sides[0] / 2) -
              1.5 * (inpdata.sides[0] / 2)
            }
            x2={
              plot_max_x +
              6 * (inpdata.sides[0] / 2) +
              1.5 * (inpdata.sides[0] / 2)
            }
            y1={plot_max_y - 1.5 * (inpdata.sides[1] + inpdata.sides[1] / 2)}
            y2={plot_max_y - 1.5 * (inpdata.sides[1] - inpdata.sides[1] / 2)}
            fillOpacity={0}
            strokeOpacity={0}
            ifOverflow="visible"
            label={{
              value: "COUNTS",
              position: "left",
              angle: -90,
              stroke: "#898989",
              dx: -5,
              opacity: 0.6,
              fontSize: 12,
            }}
          />
        )}

        {isColourBar &&
          colourRange.map((sector, index) => {
            return (
              <ReferenceArea
                key={`cb${index}`}
                x1={
                  plot_max_x +
                  6 * (inpdata.sides[0] / 2) -
                  1.5 * (inpdata.sides[0] / 2)
                }
                x2={
                  plot_max_x +
                  6 * (inpdata.sides[0] / 2) +
                  1.5 * (inpdata.sides[0] / 2)
                }
                y1={
                  plot_max_y -
                  1.5 *
                    ((COLOUR_CELLS - index + 1) * inpdata.sides[1] +
                      inpdata.sides[1] / 2)
                }
                y2={
                  plot_max_y -
                  1.5 *
                    ((COLOUR_CELLS - index + 1) * inpdata.sides[1] -
                      inpdata.sides[1] / 2)
                }
                fill={col(sector)}
                fillOpacity={0.5}
                stroke="#dadada"
                strokeOpacity={0.3}
                ifOverflow="visible"
                label={{
                  value: `${
                    index == 0
                      ? countMin
                      : index == COLOUR_CELLS
                      ? countMax
                      : ""
                  }`,
                  stroke: "#898989",
                  position: "right",
                  opacity: 0.8,
                  dx: 0,
                  fontSize: 10,
                }}
              />
            );
          })}

        {isHistogram &&
          inpdata.hist_data.map((sector, index) => {
            return (
              <ReferenceArea
                key={`hist${index}`}
                x1={sector.x - inpdata.sides[0] / 2}
                x2={sector.x + inpdata.sides[0] / 2}
                y1={sector.y - inpdata.sides[1] / 2}
                y2={sector.y + inpdata.sides[1] / 2}
                fill={col(Math.log10(sector.counts))}
                fillOpacity={0.5}
                stroke="#dadada"
                strokeOpacity={0.3}
                ifOverflow="visible"
              />
            );
          })}

        <Scatter
          data={inpdata.hist_data}
          zAxisId="invis-z"
          fill="#dadada"
          shape="square"
          opacity={0.05}
          ifOverflow="visible"
        />

        {isScatter && (
          <Scatter
            data={inpdata.scatter_data}
            zAxisId="standard"
            fill="purple"
            shape="circle"
            ifOverflow="visible"
          />
        )}
      </ScatterChart>
    </ResponsiveContainer>
  );
};
