import React, { useState, useEffect, useRef } from "react";
import { DropList } from "./DropList";
import Cookies from "js-cookie";
import { RechartsHistogram } from "./RechartsPlot";

var menu_list1 = JSON.parse(document.getElementById("menu_list").textContent);
var id = JSON.parse(document.getElementById("id").textContent);

export const API_URL = `/model/${id}/`;

const menu_keys = (arr) =>
  arr["menu"].map((d) => {
    return {
      value: d,
      label: d,
    };
  });

const labelMap = (arr) =>
  arr.map((d) => {
    return {
      value: d,
      label: d,
    };
  });

const manualPad = {
    paddingTop: "calc(0.3rem + 1px)",
    paddingBottom: "calc(0.3rem + 1px)",
    margin: "0",
    fontSize: "10px",
};

export const MenuPlot = () => {
  const menuKeys = useRef(menu_keys(menu_list1));

  const [isLoading, setIsLoading] = useState(true);

  const [currentDrop, setCurrentDrop] = useState(menuKeys.current[0]);
  const [subDropList, setSubDropList] = useState(null);
  const [initDropList, setInitDropList] = useState(null);
  const [numSamples, setNumSamples] = useState([null, null]);
  const [stridedLength, setStridedLength] = useState(null);

  const [slideSample, setSlideSample] = useState("");
  const [lockSlide, setLockSlide] = useState(false);

  const [dataXLabel, setDataXLabel] = useState(null);
  const [dataYLabel, setDataYLabel] = useState(null);
  const [data, setData] = useState(null);

  const clearDataState = () => {
    setDataXLabel(null);
    setDataYLabel(null);
    setStridedLength(null);
    setData(null);
    setLockSlide(false);
  };

  const receiveDropList = (d) => {
    const subgroupList = d["subgroup_list"];
    const initList = d["subgroup_init"];
    const num_samples = d["num_samples"];
    const strided_length = d["strided_length"];

    setSubDropList(labelMap(subgroupList));
    setInitDropList(initList);
    setNumSamples(num_samples);
    setStridedLength(strided_length);
    setSlideSample(strided_length);
  };

  const receiveNewData = (d) => {
    setData(d["trunc_data"]);
    setNumSamples(d["num_samples"]);
  };

  const requestHandler = (evt, key, fn, ...fn_kwargs) => {
    const csrftoken = Cookies.get("csrftoken");
    const formData = new FormData();

    if (Array.isArray(evt)) {
      evt.forEach((e) => formData.append(key, e));
    } else {
      formData.append(key, evt);
    }

    fetch(API_URL, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrftoken,
        // 'Content-Type': 'application/json',
        // 'Accept': 'application/json'
      },
      credentials: "include",
      body: formData,
    })
      .then((res) => res.json())
      .then((d) =>
        setIsLoading(false) && fn_kwargs ? fn(d, fn_kwargs) : fn(d)
      )
      .catch((err) => console.log(err));
  };

  useEffect(() => {
    setIsLoading(true);
    requestHandler(currentDrop.value, "main_group", receiveDropList);
    clearDataState();
  }, [currentDrop]);

  useEffect(() => {
    if (subDropList != null && initDropList != null) {
      setDataXLabel(subDropList[initDropList[0]]);
      setDataYLabel(subDropList[initDropList[1]]);
    }
  }, [initDropList]);

  useEffect(() => {
    if (dataXLabel != null && dataYLabel != null && stridedLength != null) {
      requestHandler(
        [currentDrop.value, dataXLabel.value, dataYLabel.value, stridedLength],
        "data_request",
        receiveNewData
      );
    }
  }, [dataXLabel, dataYLabel, stridedLength]);

  useEffect(() => {
    if (lockSlide) {
      const timeOutId = setTimeout(() => setStridedLength(slideSample), 2000);
      return () => clearTimeout(timeOutId);
    }
  }, [slideSample]);

  return (
    <div>
      <div id="tooltip-panel">
        <div>
          <DropList
            data={menuKeys.current}
            value={currentDrop}
            onChange={(a) => {
              requestHandler(a.value, "main_group", receiveDropList);
              setCurrentDrop(a);
            }}
          />
        </div>
        {subDropList != null && (
          <>
            <div>
              <DropList
                data={subDropList}
                value={dataXLabel}
                onChange={(a) => {
                  setDataXLabel(a);
                }}
              />
            </div>
            <div>
              <DropList
                data={subDropList}
                value={dataYLabel}
                onChange={(a) => {
                  setDataYLabel(a);
                }}
              />
            </div>
          </>
        )}

        <div>
          {numSamples[1] && (
            <div className="mb-3 row form-outline">
              <div style={manualPad} className="col-sm-4">
                <input
                  type="range"
                  className="form-range"
                  value={slideSample}
                  min="1"
                  max={Math.max(10, Math.floor(numSamples[1] / 1e5))}
                  step="1"
                  disabled={!lockSlide}
                  onChange={(d) => setSlideSample(d.target.value)}
                ></input>
              </div>
              <div className="col-sm-2">
                <label className="col-form-label">{`${slideSample}`}</label>
              </div>
              <div className="col-sm-1">
                <div style={manualPad} className="form-check float-end">
                  <input
                    className="form-check-input"
                    type="checkbox"
                    value={lockSlide}
                    id="flexCheckDefault"
                    onChange={(d) => {
                      setLockSlide(d.target.checked);
                    }}
                  />
                </div>
              </div>
              <div className="col-sm-5">
                <label className="col-form-label">
                  Sample every n other datapoint (Improves Performance for
                  exceptionally large datasets)
                </label>
              </div>
            </div>
          )}
        </div>
      </div>

      <div
        className="d-flex justify-content-center align-items-center"
        style={{ height: 60 + "px" }}
      >
        {isLoading ? (
          <div
            className="spinner-border text-muted"
            style={{ width: 3 + "rem", height: 3 + "rem" }}
            role="status"
          ></div>
        ) : (
          <div className="text-muted">
            <span>{`${numSamples[0]} entries out of ${numSamples[1]} entries total`}</span>
          </div>
        )}
      </div>
      {data != null && (
        <RechartsHistogram
          inpdata={data}
          axis={[dataXLabel.value, dataYLabel.value]}
        />
      )}
    </div>
  );
};
