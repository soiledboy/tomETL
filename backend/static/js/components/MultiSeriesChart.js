import React from "react";
// import { CityTemperature } from "@visx/mock-data/lib/mocks/cityTemperature";
import {
  AnimatedAnnotation,
  AnimatedAxis,
  AnimatedGrid,
  AnimatedLineSeries,
  AnnotationCircleSubject,
  AnnotationConnector,
  AnnotationLabel,
  AnnotationLineSubject,
  Tooltip,
  XYChart
} from "@visx/xychart";
import ExampleControls from "./ExampleControls";
import CustomChartBackground from "./CustomChartBackground";


const getDate = (d) => d.date;
const getValue = (d) => d.value;


export default function MultiSeriesChart({ height, width, xdata }) {
  return (
    <ExampleControls>
      {({
        accessors,
        animationTrajectory,
        annotationDataKey,
        annotationDatum,
        annotationLabelPosition,
        annotationType,
        config,
        data,
        editAnnotationLabelPosition,
        numTicks,
        renderBarGroup,
        renderHorizontally,
        setAnnotationDataIndex,
        setAnnotationDataKey,
        setAnnotationLabelPosition,
        sharedTooltip,
        showGridColumns,
        showGridRows,
        showHorizontalCrosshair,
        showTooltip,
        showVerticalCrosshair,
        snapTooltipToDatumX,
        snapTooltipToDatumY,
        theme,
        xAxisOrientation,
        yAxisOrientation
      }) => (
        <XYChart
          theme={theme}
          xScale={config.x}
          yScale={config.y}
          height={Math.min(400, height)}
          captureEvents={!editAnnotationLabelPosition}
          onPointerUp={(d) => {
            setAnnotationDataKey(d.key);
            setAnnotationDataIndex(d.index);
          }}
        >
          <CustomChartBackground />
          <AnimatedGrid
            key={`grid-${animationTrajectory}`} // force animate on update
            rows={showGridRows}
            columns={showGridColumns}
            animationTrajectory={animationTrajectory}
            numTicks={numTicks}
          />
          {/* add data series */}
          <>
            {xdata.map(x => {
              return <AnimatedLineSeries 
                dataKey={x.name}
                key={x.name} 
                data={x.series} 
                xAccessor={getDate}
                yAccessor={getValue}
              />
            })}
          </>
          {/* axis configurations */}
          <AnimatedAxis
            key={`price-axis-${animationTrajectory}-${renderHorizontally}`}
            orientation={yAxisOrientation}
            numTicks={numTicks}
            animationTrajectory={animationTrajectory}
            label={"Price ($USD)"}
          />
          <AnimatedAxis
            key={`time-axis-${animationTrajectory}-${renderHorizontally}`}
            label="Date"
            orientation={xAxisOrientation}
            numTicks={numTicks}
            animationTrajectory={animationTrajectory}
          />
          
          <AnimatedAnnotation
            dataKey={annotationDataKey}
            datum={annotationDatum}
            dx={annotationLabelPosition.dx}
            dy={annotationLabelPosition.dy}
            editable={editAnnotationLabelPosition}
            canEditSubject={false}
            onDragEnd={({ dx, dy }) => setAnnotationLabelPosition({ dx, dy })}
          >
            <AnnotationConnector />
            <AnnotationCircleSubject />
            <AnnotationLabel
              title={annotationDataKey}
              subtitle={`${annotationDatum.date}, $${annotationDatum[annotationDataKey]}`}
              width={135}
              backgroundProps={{
                stroke: theme.gridStyles.stroke,
                strokeOpacity: 0.5,
                fillOpacity: 0.8
              }}
            />
          </AnimatedAnnotation>
          
          {showTooltip && (
            <Tooltip
              showHorizontalCrosshair={showHorizontalCrosshair}
              showVerticalCrosshair={showVerticalCrosshair}
              snapTooltipToDatumX={snapTooltipToDatumX}
              snapTooltipToDatumY={snapTooltipToDatumY}
              showDatumGlyph={
                (snapTooltipToDatumX || snapTooltipToDatumY)
              }
              showSeriesGlyphs={sharedTooltip}
              renderTooltip={({ tooltipData, colorScale }) => (
                <>
                  { console.log(tooltipData) }
                  {/** date */}
                  {(tooltipData?.nearestDatum?.datum &&
                    accessors.date(tooltipData?.nearestDatum?.datum)) ||
                    "No date"}
                  <br />
                  <br />
                  {/** temperatures */}
                  {((sharedTooltip
                    ? Object.keys(tooltipData?.datumByKey ?? {})
                    : [tooltipData?.nearestDatum?.key]
                  ).filter((name) => name)).map((name) => (
                    <div key={name}>
                      <em
                        style={{
                          color: colorScale?.(name),
                          textDecoration:
                            tooltipData?.nearestDatum?.key === name
                              ? "underline"
                              : undefined
                        }}
                      >
                        {name}
                      </em>{" "}
                      {tooltipData?.datumByKey[name]?.datum?.value}
                    </div>
                  ))}
                </>
              )}
            />
          )}
        </XYChart>
      )}
    </ExampleControls>
  );
}
