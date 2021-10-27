import React, {useState, useEffect, useRef} from 'react';
import {
    XYPlot,
    XAxis,
    YAxis, 
    HexbinSeries, 
    Hint, 
    Highlight, 
    Borders, 
    ContinuousColorLegend} from 'react-vis';
import { ShowcaseButton } from './ButtonContent';
import { DropList } from './DropList';
import { format } from 'd3-format';
import 'react-vis/es/main.scss';

export const InteractivePlot = ({
        data,
        axisdata,
    }) => {

        const dataKeys = useRef(Object.keys(data[0]));

        const [animationHook, setAnimationHook] = useState("gentle");
        const [hoveredHook, setHoveredHook] = useState(1);
        const [hoveredNode, setHoveredNode] = useState(null);
        const [dataX, setdataX] = useState(dataKeys.current[0]);
        const [dataY, setdataY] = useState(dataKeys.current[1]);

        const [countHex, setCountHex] = useState([0,0]);
        const countHexTest = useRef([0,0]);

        const [lastDrawLocation, setLastDrawLocation] = useState(null);
        const [radius, setRadius] = useState(5);

        const updateData = data.map(d => ({
            x: Number(d[dataX]),
            y: Number(d[dataY])
        }));

        const asyncKeys = dataKeys.current.map(d => {
            return {
                value: d,
                label: d
            }          
        });

        const convKey = (d) => {
            return {
                value: d,
                label: d
            }
        };

        const xAxisFormatter = (value, index, scale, tickTotal) => {
            return `${(scale.tickFormat(tickTotal, '.2')(value / 10 ** (Math.round(Math.log10(Math.min(...axisdata[dataX]))))))}`;
        }

        const yAxisFormatter = (value, index, scale, tickTotal) => {
            return `${(scale.tickFormat(tickTotal, '.2')(value / 10 ** (Math.round(Math.log10(Math.min(...axisdata[dataY]))))))}`;
        }
          
        useEffect(() => {
            //console.log(updateData);
            //console.log(format("+04")(22));
            //console.log(5, HexbinSeries.prototype);
        }, []);

        useEffect(() => {
            console.log(hoveredHook);
        }, [hoveredHook]);

        useEffect(() => {
            console.log(countHexTest.current);
            //setCountHex(countHexTest.current);
        }, [updateData]);

        return(
            <div>
                <div id='tooltip-panel' style={{display:'flex'}}>
                    <div style={{order:5}}>
                    <ShowcaseButton
                        onClick={() => setLastDrawLocation(null)}
                        buttonContent={'Reset'}
                    />
                    </div>
                    <div style={{width: '200px'}}>
                    <DropList
                        data={asyncKeys}
                        defaultValue={convKey(dataX)}
                        onChange={(a) => {
                            setdataX(a.value);
                        }}
                    />
                    </div>
                    <div style={{width: '200px'}}>
                    <DropList
                        data={asyncKeys}
                        defaultValue={convKey(dataY)}
                        onChange={(a) => {
                            setdataY(a.value);
                        }}
                    />
                    </div>
                </div>

                <div id='plot-container'>
                    <XYPlot
                        xDomain={ lastDrawLocation ?
                            [
                                lastDrawLocation.left,
                                lastDrawLocation.right
                            ] :
                                axisdata[dataX]                    
                        }
                        yDomain={ lastDrawLocation ?
                            [
                                lastDrawLocation.bottom,
                                lastDrawLocation.top
                            ] :
                                axisdata[dataY]
                        }
                        width={500}
                        onMouseLeave={() => setHoveredNode(null)}
                        height={500}
                    >
                        <Highlight
                            onBrushEnd={area => {
                                setHoveredHook(1);
                                setLastDrawLocation(area);
                            }}
                            onBrushStart={() => setHoveredHook(0)}
                            onDrag={area => { 
                                setLastDrawLocation({
                                    lastDrawLocation: {
                                        bottom: lastDrawLocation.bottom + (area.top - area.bottom),
                                        left: lastDrawLocation.left - (area.right - area.left),
                                        right: lastDrawLocation.right - (area.right - area.left),
                                        top: lastDrawLocation.top + (area.top - area.bottom)
                                    }
                                });
                            }}
                        />

                        <HexbinSeries
                            animation={animationHook}
                            style={{
                            pointerEvents: hoveredHook ? '' : 'none',
                            stroke: '#125C77',
                            strokeLinejoin: 'round'
                            }}
                            onValueMouseOver={d => {
                                setHoveredNode(d)
                                setAnimationHook('');
                            }}
                            onValueMouseOut={() => {
                                setHoveredNode(null);
                                setAnimationHook('gentle');
                            }}
                            colorRange={['orange', 'cyan']}
                            radius={radius}
                            data={updateData}
                            countData={d => countHexTest.current = d}
                        />

                        {hoveredNode && ( 
                            <Hint 
                                xType="literal"
                                yType="literal"
                                value={{
                                    x: hoveredNode.x,
                                    y: hoveredNode.y,
                                    value: hoveredNode.length
                            }}/> 
                        )}

                        <Borders style={{all: {fill: '#fafafa'}}} />

                        <XAxis 
                            title={`${dataX} (e${format("+03")(Math.round(Math.log10(Math.min(...axisdata[dataX]))))})`}
                            tickFormat={xAxisFormatter}
                        />
                        
                        <YAxis 
                            title={`${dataY} (e${format("+03")(Math.round(Math.log10(Math.min(...axisdata[dataY]))))})`}
                            tickFormat={yAxisFormatter}
                        />

                    </XYPlot>

                    <ContinuousColorLegend
                            height={500}
                            width={200}
                            startColor='orange'
                            endColor='cyan'
                            startTitle={countHex[0]}
                            endTitle={countHex[1]}
                            orient='vertical'
                    />
                </div> 
            </div>
        );

};