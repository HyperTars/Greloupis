import React from "react";
import { Empty } from "antd";

function EmptyPage() {
  const emptyPage = (
    <div className="EmptyData">
      <Empty
        image={Empty.PRESENTED_IMAGE_SIMPLE}
        imageStyle={{ height: 90 }}
        description={<span></span>}
      ></Empty>
      <div>
        <h1>{"404 NOT FOUND"}</h1>
      </div>
    </div>
  );

  return emptyPage;
}

export default EmptyPage;
