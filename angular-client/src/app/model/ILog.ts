import { ILogId } from "./ILogId";

export interface ILog {
  _id: ILogId;
  timestamp?: Date;
  hostname?: string;
  appname?: string;
  procid?: string;
  msgid?: string;
  msg?: string;
  version?: number;
  severity?: number;
  facility?: number;
  line?: number;
}
