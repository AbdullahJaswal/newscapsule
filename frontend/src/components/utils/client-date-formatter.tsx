"use client";

import Moment from "react-moment";

type Props = {
  date: string;
};

export default function ClientDateFormatter(props: Props) {
  return <Moment fromNow>{props.date}</Moment>;
}
