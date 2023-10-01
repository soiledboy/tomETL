import React from "react";
import { BarStackHorizontal } from "@visx/shape";
import { Group } from "@visx/group";
import { AxisBottom, AxisLeft } from "@visx/axis";
import { scaleBand, scaleLinear, scaleOrdinal } from "@visx/scale";
import { withTooltip, Tooltip, defaultStyles } from "@visx/tooltip";
import { Grid } from "@visx/grid";


const purple1 = "#6c5efb";
const purple2 = "#c998ff";
export const purple3 = "#a44afe";
export const background = "#eaedff";

const gridColor = "black"

const defaultMargin = { top: 40, left: 50, right: 40, bottom: 100 };

const tooltipStyles = {
  ...defaultStyles,
  minWidth: 60,
  backgroundColor: "rgba(0,0,0,0.9)",
  color: "white",
  justifyContent: "center"
};

let tooltipTimeout;

export default withTooltip(
  ({
    xdata,
    sortData = false,
    width,
    height,
    events = false,
    margin = defaultMargin,
    tooltipOpen,
    tooltipLeft,
    tooltipTop,
    tooltipData,
    title,
    hideTooltip,
    showTooltip
  }) => {

    const titleStyles = {
      position: "absolute",
      top: margin.top / 2 - 10,
      width: width,
      display: "flex",
      justifyContent: "center",
      fontSize: "14px",
      color: "black",
    }
    
    // bounds
    const xMax = width - margin.left - margin.right;
    const yMax = height - margin.top - margin.bottom;

    let data = xdata.map((d) => {
      return {
        name: d.name,
        Price: d.value,
      }
    })

    if (sortData) {
      data = data.sort((a, b) => a.Price - b.Price)
    }

    const keys = Object.keys(data[0]).filter((d) => d !== "name");
    
    const temperatureTotals = data.reduce((allTotals, currentDate) => {
      const totalTemperature = keys.reduce((dailyTotal, k) => {
        dailyTotal += Number(currentDate[k]);
        return dailyTotal;
      }, 0);
      allTotals.push(totalTemperature);
      return allTotals;
    }, []);

    // accessors
    const getName = (d) => d.name;

    // scales
    const temperatureScale = scaleLinear({
      domain: [Math.min(...temperatureTotals)-1, Math.max(...temperatureTotals)+1],
      nice: false
    });

    const dateScale = scaleBand({
      domain: data.map(getName),
      padding: 0.1
    });

    const colorScale = scaleOrdinal({
      domain: keys,
      range: [purple1, purple2, purple3]
    });

    temperatureScale.rangeRound([0, xMax]);
    dateScale.rangeRound([yMax, 0]);

    return (
      <div>
        <svg width={width} height={height}>
          <rect width={width} height={height} fill={background} rx={14} />
          <Grid
            top={margin.top}
            left={margin.left}
            xScale={temperatureScale}
            yScale={dateScale}
            width={width-margin.left-margin.right}
            height={yMax}
            stroke={gridColor}
            strokeOpacity={0.1}
          />
          <Group top={margin.top} left={margin.left}>
            <BarStackHorizontal
              data={data}
              keys={keys}
              height={yMax}
              y={getName}
              xScale={temperatureScale}
              yScale={dateScale}
              color={colorScale}
              offset={'diverging'}
            >
              {(barStacks) =>
                barStacks.map((barStack) =>
                  barStack.bars.map((bar) => (
                    <rect
                      key={`barstack-horizontal-${barStack.index}-${bar.index}`}
                      x={bar.x}
                      y={bar.y}
                      width={bar.width}
                      height={bar.height}
                      fill={bar.color}
                      onClick={() => {
                        if (events) console.log(`clicked: ${JSON.stringify(bar)}`);
                      }}
                      onMouseLeave={() => {
                        tooltipTimeout = window.setTimeout(() => {
                          hideTooltip();
                        }, 300);
                      }}
                      onMouseMove={() => {
                        if (tooltipTimeout) clearTimeout(tooltipTimeout);
                        const top = bar.y + margin.top;
                        const left = bar.x + margin.left;
                        showTooltip({
                          tooltipData: bar,
                          tooltipTop: top,
                          tooltipLeft: left
                        });
                      }}
                    />
                  ))
                )
              }
            </BarStackHorizontal>
            <AxisLeft
              hideAxisLine
              hideTicks
              scale={dateScale}
              // tickFormat={formatDate}
              stroke={gridColor}
              tickStroke={ gridColor }
              tickLabelProps={() => ({
                fill: gridColor,
                fontSize: 11,
                textAnchor: "end",
                dy: "0.33em"
              })}
            />
            <AxisBottom
              top={yMax}
              scale={temperatureScale}
              stroke={gridColor}
              tickStroke={gridColor}
              tickLabelProps={() => ({
                fill: gridColor,
                fontSize: 11,
                textAnchor: "middle"
              })}
            />
          </Group>
        </svg>
        <div style={titleStyles}>
          {title && (<content className="barChart-title">{title}</content>)}
        </div>
        {tooltipOpen && tooltipData && (
          <Tooltip top={tooltipTop} left={tooltipLeft} style={tooltipStyles}>
            {/* <div style={{ color: colorScale(tooltipData.key) }}>
              <strong>{tooltipData.key}</strong>
            </div> */}
            <div>{tooltipData.bar.data[tooltipData.key]}</div>
            {/* <div>
              <small>{getDate(tooltipData.bar.data)}</small>
            </div> */}
          </Tooltip>
        )}
      </div>
    );
  }
);

