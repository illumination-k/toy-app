import React, {
  createContext,
  useContext,
  useState,
  Dispatch,
  SetStateAction,
} from "react";
import "./App.css";

import useSWR from "swr";
import axios from "axios";
import { useForm } from "react-hook-form";

const fetcher = (url: string) => fetch(url).then((r) => r.json());

type Message = {
  message: string;
};

type Query = {
  query: string;
};

type Config = {
  baseUrl: string;
  query: string | undefined;
};

const config2url = (config: Config) => {
  if (config.query) {
    return `${config.baseUrl}?q=${config.query}`;
  }

  return config.baseUrl;
};
const BASE_URL = "http://localhost:8002/message";
const BaseConfig: Config = {
  baseUrl: BASE_URL,
  query: undefined,
};

const ConfigContext = createContext(BaseConfig);

const TimeLine = () => {
  const config = useContext(ConfigContext);

  const { data, error } = useSWR(config2url(config), fetcher, {
    refreshInterval: 500,
  });

  if (error) {
    return <div>{JSON.stringify(error)}</div>;
  }

  if (!data) {
    return <div>Loading</div>;
  }

  return <div>{JSON.stringify(data)}</div>;
};

const PostMessage = () => {
  const { register, handleSubmit } = useForm<Message>();

  const onSubmit = (data: Message) => {
    axios.post(BASE_URL, { message: data.message });
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <label>Input Your Message</label>
      <input {...register("message")} />
      <input type="submit" />
    </form>
  );
};

const SearchMessage: React.VFC<{
  setConfig: Dispatch<SetStateAction<Config>>;
}> = ({ setConfig }) => {
  const config = useContext(ConfigContext);
  const { register, handleSubmit } = useForm<Query>();

  const onSubmit = (data: Query) => {
    setConfig({ ...config, query: data.query });
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <label>Search</label>
      <input {...register("query")} />
      <input type="submit" />
    </form>
  );
};

function App() {
  const [config, setConfig] = useState<Config>(BaseConfig);
  console.log(config, config2url(config));

  return (
    <div className="App">
      <ConfigContext.Provider value={config}>
        <PostMessage />
        <SearchMessage setConfig={setConfig} />
        <TimeLine />
      </ConfigContext.Provider>
    </div>
  );
}

export default App;
