import { useState } from "react";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const API_URL =
  import.meta.env.VITE_API_URL || "/api";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const [datasetId, setDatasetId] = useState(null);
  const [datasetName, setDatasetName] = useState("");
  const [uploading, setUploading] = useState(false);

  const [profile, setProfile] = useState(null);
  const [analyticsResult, setAnalyticsResult] = useState(null);

  const uploadDataset = async (event) => {
    const file = event.target.files[0];

    if (!file) return;

    setUploading(true);
    setAnswer("");
    setAnalyticsResult(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(
        `${API_URL}/datasets/upload`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Upload failed");
      }

      setDatasetId(data.dataset_id);
      setDatasetName(data.filename);
      setProfile(data.profile);

      setAnswer(
        "Dataset uploaded successfully. You can now ask questions about it."
      );
    } catch (error) {
      setAnswer(`Error: ${error.message}`);
    }

    setUploading(false);
  };

  const askAI = async () => {
    if (!question.trim()) return;

    if (!datasetId) {
      setAnswer("Please upload a dataset first.");
      return;
    }

    setLoading(true);
    setAnswer("");
    setAnalyticsResult(null);

    try {
      const response = await fetch(
        `${API_URL}/ai/ask`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            dataset_id: datasetId,
            question: question,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Something went wrong"
        );
      }

      setAnswer(data.answer);
      setAnalyticsResult(data.analytics_result);
    } catch (error) {
      setAnswer(`Error: ${error.message}`);
    }

    setLoading(false);
  };

  const resetDataset = () => {
    setDatasetId(null);
    setDatasetName("");
    setProfile(null);
    setQuestion("");
    setAnswer("");
    setAnalyticsResult(null);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white">

      {/* Header */}
      <header className="border-b border-slate-800">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-8 py-5">

          <div>
            <h1 className="text-2xl font-bold">
              InsightFlow{" "}
              <span className="text-blue-400">
                AI
              </span>
            </h1>

            <p className="text-sm text-slate-400">
              AI-Powered Data Analytics Platform
            </p>
          </div>

          <div className="rounded-full border border-green-500/30 bg-green-500/10 px-4 py-2 text-sm text-green-400">
            ● System Online
          </div>

        </div>
      </header>


      {/* Main */}
      <main className="mx-auto max-w-7xl px-8 py-10">

        {/* Hero */}
        <section className="mb-8">

          <div className="max-w-3xl">

            <div className="mb-3 inline-flex rounded-full border border-blue-500/20 bg-blue-500/10 px-3 py-1 text-xs text-blue-400">
              RAG • Analytics • LLM
            </div>

            <h2 className="text-4xl font-bold tracking-tight">
              Turn your data into
              <span className="text-blue-400">
                {" "}insights
              </span>
            </h2>

            <p className="mt-3 text-slate-400">
              Upload a dataset, explore its quality and statistics,
              and ask natural-language questions powered by
              analytics, retrieval, and large language models.
            </p>

          </div>

        </section>


        {/* Upload Dataset */}
        <section className="rounded-xl border border-slate-800 bg-slate-900 p-8">

          <div className="flex items-center justify-between">

            <div>
              <h3 className="text-xl font-semibold">
                Upload Dataset
              </h3>

              <p className="mt-1 text-sm text-slate-400">
                Supported formats: CSV and Excel
              </p>
            </div>

            {datasetId && (
              <button
                onClick={resetDataset}
                className="rounded-lg border border-slate-700 px-4 py-2 text-sm text-slate-300 transition hover:bg-slate-800"
              >
                New Dataset
              </button>
            )}

          </div>


          <label className="mt-6 flex cursor-pointer items-center justify-center rounded-lg border-2 border-dashed border-slate-700 bg-slate-950 px-6 py-10 transition hover:border-blue-500">

            <div className="text-center">

              <div className="text-3xl">
                📊
              </div>

              <p className="mt-3 font-medium">
                {uploading
                  ? "Uploading dataset..."
                  : "Click to upload your dataset"}
              </p>

              <p className="mt-1 text-sm text-slate-500">
                CSV or XLSX
              </p>

            </div>

            <input
              type="file"
              accept=".csv,.xlsx"
              onChange={uploadDataset}
              className="hidden"
            />

          </label>


          {datasetName && (
            <div className="mt-5 flex items-center justify-between rounded-lg border border-green-500/20 bg-green-500/10 p-4">

              <div>
                <p className="text-sm text-green-400">
                  Dataset loaded
                </p>

                <p className="mt-1 font-medium">
                  {datasetName}
                </p>
              </div>

              <span className="text-xl">
                ✓
              </span>

            </div>
          )}

        </section>


        {/* Statistics */}
        {profile && (
          <section className="mt-8 grid gap-5 md:grid-cols-4">

            <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">
              <p className="text-sm text-slate-400">
                Rows
              </p>

              <p className="mt-2 text-3xl font-bold">
                {profile.rows.toLocaleString()}
              </p>
            </div>


            <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">
              <p className="text-sm text-slate-400">
                Columns
              </p>

              <p className="mt-2 text-3xl font-bold">
                {profile.columns}
              </p>
            </div>


            <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">
              <p className="text-sm text-slate-400">
                Duplicate Rows
              </p>

              <p className="mt-2 text-3xl font-bold">
                {profile.duplicate_rows}
              </p>
            </div>


            <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">
              <p className="text-sm text-slate-400">
                AI Engine
              </p>

              <p className="mt-2 text-xl font-bold text-blue-400">
                RAG + LLM
              </p>
            </div>

          </section>
        )}


        {/* Analytics Dashboard */}
        {profile && (
          <section className="mt-8 rounded-xl border border-slate-800 bg-slate-900 p-8">

            <div className="mb-8">
              <h3 className="text-xl font-semibold">
                Analytics Dashboard
              </h3>

              <p className="mt-1 text-sm text-slate-400">
                Visual summary of your dataset
              </p>
            </div>


            <div>

              <h4 className="mb-4 font-medium text-slate-200">
                Missing Values by Column
              </h4>

              <div className="h-80 w-full">

                <ResponsiveContainer
                  width="100%"
                  height="100%"
                >

                  <BarChart
                    data={profile.column_details.map(
                      (column) => ({
                        name: column.name,
                        missing: column.missing_values,
                      })
                    )}
                  >

                    <CartesianGrid
                      strokeDasharray="3 3"
                      stroke="#334155"
                    />

                    <XAxis
                      dataKey="name"
                      tick={{
                        fill: "#94a3b8",
                        fontSize: 12,
                      }}
                      angle={-25}
                      textAnchor="end"
                      height={70}
                    />

                    <YAxis
                      tick={{
                        fill: "#94a3b8",
                      }}
                    />

                    <Tooltip />

                    <Bar
                      dataKey="missing"
                      fill="#3b82f6"
                      radius={[6, 6, 0, 0]}
                    />

                  </BarChart>

                </ResponsiveContainer>

              </div>

            </div>


            {/* Numerical Statistics */}
            <div className="mt-10">

              <h4 className="mb-4 font-medium text-slate-200">
                Numerical Statistics
              </h4>

              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">

                {profile.column_details
                  .filter(
                    (column) => column.statistics
                  )
                  .map((column) => (

                    <div
                      key={column.name}
                      className="rounded-lg border border-slate-800 bg-slate-950 p-5"
                    >

                      <h5 className="font-semibold text-white">
                        {column.name}
                      </h5>

                      <div className="mt-4 space-y-2 text-sm">

                        <div className="flex justify-between">
                          <span className="text-slate-500">
                            Mean
                          </span>

                          <span className="text-slate-300">
                            {column.statistics.mean}
                          </span>
                        </div>

                        <div className="flex justify-between">
                          <span className="text-slate-500">
                            Median
                          </span>

                          <span className="text-slate-300">
                            {column.statistics.median}
                          </span>
                        </div>

                        <div className="flex justify-between">
                          <span className="text-slate-500">
                            Minimum
                          </span>

                          <span className="text-slate-300">
                            {column.statistics.minimum}
                          </span>
                        </div>

                        <div className="flex justify-between">
                          <span className="text-slate-500">
                            Maximum
                          </span>

                          <span className="text-slate-300">
                            {column.statistics.maximum}
                          </span>
                        </div>

                      </div>

                    </div>

                  ))}

              </div>

            </div>

          </section>
        )}


        {/* Dataset Profile */}
        {profile && (
          <section className="mt-8 rounded-xl border border-slate-800 bg-slate-900 p-8">

            <div className="flex items-center justify-between">

              <div>

                <h3 className="text-xl font-semibold">
                  Dataset Profile
                </h3>

                <p className="mt-1 text-sm text-slate-400">
                  Data quality and column-level information
                </p>

              </div>

              <div className="rounded-full bg-blue-500/10 px-4 py-2 text-sm text-blue-400">
                {profile.column_details.length} Columns
              </div>

            </div>


            <div className="mt-6 overflow-x-auto">

              <table className="w-full text-left text-sm">

                <thead className="border-b border-slate-800 text-slate-400">

                  <tr>

                    <th className="px-4 py-3">
                      Column
                    </th>

                    <th className="px-4 py-3">
                      Data Type
                    </th>

                    <th className="px-4 py-3">
                      Semantic Type
                    </th>

                    <th className="px-4 py-3">
                      Missing
                    </th>

                    <th className="px-4 py-3">
                      Unique
                    </th>

                  </tr>

                </thead>


                <tbody>

                  {profile.column_details.map(
                    (column) => (

                      <tr
                        key={column.name}
                        className="border-b border-slate-800/60 hover:bg-slate-800/40"
                      >

                        <td className="px-4 py-4 font-medium text-white">
                          {column.name}
                        </td>

                        <td className="px-4 py-4 text-slate-400">
                          {column.data_type}
                        </td>

                        <td className="px-4 py-4">

                          <span className="rounded-md bg-slate-800 px-2 py-1 text-xs text-blue-300">
                            {column.semantic_type}
                          </span>

                        </td>

                        <td className="px-4 py-4">

                          <span
                            className={
                              column.missing_values > 0
                                ? "text-yellow-400"
                                : "text-green-400"
                            }
                          >
                            {column.missing_values}
                          </span>

                        </td>

                        <td className="px-4 py-4 text-slate-400">
                          {column.unique_values}
                        </td>

                      </tr>

                    )
                  )}

                </tbody>

              </table>

            </div>

          </section>
        )}


        {/* Ask AI */}
        <section className="mt-8 rounded-xl border border-slate-800 bg-slate-900 p-8">

          <div className="flex items-center justify-between">

            <div>

              <h3 className="text-xl font-semibold">
                Ask InsightFlow AI
              </h3>

              <p className="mt-1 text-sm text-slate-400">
                Ask anything about your uploaded dataset.
              </p>

            </div>

            <div className="hidden rounded-full border border-blue-500/20 bg-blue-500/10 px-3 py-1 text-xs text-blue-400 sm:block">
              AI Ready
            </div>

          </div>


          <div className="mt-6 flex gap-3">

            <input
              type="text"
              value={question}
              onChange={(e) =>
                setQuestion(e.target.value)
              }
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  askAI();
                }
              }}
              placeholder="e.g. What is the average temperature?"
              className="flex-1 rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-blue-500"
            />


            <button
              onClick={askAI}
              disabled={loading || !datasetId}
              className="rounded-lg bg-blue-600 px-6 py-3 font-medium transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading
                ? "Analyzing..."
                : "Ask AI"}
            </button>

          </div>


          {/* Example Questions */}
          {profile && (

            <div className="mt-5 flex flex-wrap gap-3">

              <button
                onClick={() =>
                  setQuestion(
                    "What is the average temperature?"
                  )
                }
                className="rounded-lg border border-slate-700 px-3 py-2 text-sm text-slate-400 transition hover:bg-slate-800"
              >
                Average Temperature
              </button>


              <button
                onClick={() =>
                  setQuestion(
                    "What is the maximum pressure?"
                  )
                }
                className="rounded-lg border border-slate-700 px-3 py-2 text-sm text-slate-400 transition hover:bg-slate-800"
              >
                Maximum Pressure
              </button>


              <button
                onClick={() =>
                  setQuestion(
                    "What is the minimum vibration?"
                  )
                }
                className="rounded-lg border border-slate-700 px-3 py-2 text-sm text-slate-400 transition hover:bg-slate-800"
              >
                Minimum Vibration
              </button>


              <button
                onClick={() =>
                  setQuestion(
                    "How many faulty sensors are there?"
                  )
                }
                className="rounded-lg border border-slate-700 px-3 py-2 text-sm text-slate-400 transition hover:bg-slate-800"
              >
                Faulty Sensors
              </button>


              <button
                onClick={() =>
                  setQuestion(
                    "What is the correlation between temperature and pressure?"
                  )
                }
                className="rounded-lg border border-slate-700 px-3 py-2 text-sm text-slate-400 transition hover:bg-slate-800"
              >
                Temperature vs Pressure
              </button>


              <button
                onClick={() =>
                  setQuestion(
                    "How many rows are in the dataset?"
                  )
                }
                className="rounded-lg border border-slate-700 px-3 py-2 text-sm text-slate-400 transition hover:bg-slate-800"
              >
                Dataset Size
              </button>


              <button
                onClick={() =>
                  setQuestion(
                    "Show me the missing values in the dataset."
                  )
                }
                className="rounded-lg border border-slate-700 px-3 py-2 text-sm text-slate-400 transition hover:bg-slate-800"
              >
                Missing Values
              </button>

            </div>

          )}

        </section>


        {/* AI Response */}
        <section className="mt-8 rounded-xl border border-slate-800 bg-slate-900 p-8">

          <div className="flex items-center gap-3">

            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-600">
              AI
            </div>

            <div>

              <h3 className="font-semibold">
                InsightFlow Response
              </h3>

              <p className="text-xs text-slate-500">
                RAG + Analytics + LLM
              </p>

            </div>

          </div>


          {/* Verified Analytics */}
          {analyticsResult && (

            <div className="mt-6 rounded-lg border border-blue-500/20 bg-blue-500/5 p-5">

              <div className="flex items-center justify-between">

                <h4 className="font-semibold text-blue-400">
                  Verified Analytics
                </h4>

                <span className="rounded-full bg-blue-500/10 px-3 py-1 text-xs text-blue-400">
                  Python / Pandas
                </span>

              </div>


              <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">

                {analyticsResult.type === "calculation" && (
                  <>
                    <div>
                      <p className="text-xs text-slate-500">
                        Operation
                      </p>

                      <p className="mt-1 font-medium text-white">
                        {analyticsResult.operation}
                      </p>
                    </div>


                    <div>
                      <p className="text-xs text-slate-500">
                        Column
                      </p>

                      <p className="mt-1 font-medium text-white">
                        {analyticsResult.column}
                      </p>
                    </div>


                    <div>
                      <p className="text-xs text-slate-500">
                        Result
                      </p>

                      <p className="mt-1 text-xl font-bold text-blue-400">
                        {analyticsResult.value}
                      </p>
                    </div>
                  </>
                )}


                {analyticsResult.type === "fault_analysis" && (
                  <>
                    <div>
                      <p className="text-xs text-slate-500">
                        Faulty Sensors
                      </p>

                      <p className="mt-1 text-xl font-bold text-red-400">
                        {analyticsResult.faulty_sensors}
                      </p>
                    </div>


                    <div>
                      <p className="text-xs text-slate-500">
                        Total Records
                      </p>

                      <p className="mt-1 text-xl font-bold text-white">
                        {analyticsResult.total_records}
                      </p>
                    </div>


                    <div>
                      <p className="text-xs text-slate-500">
                        Fault Percentage
                      </p>

                      <p className="mt-1 text-xl font-bold text-yellow-400">
                        {analyticsResult.fault_percentage}%
                      </p>
                    </div>
                  </>
                )}


                {analyticsResult.type === "dataset_size" && (
                  <>
                    {analyticsResult.rows !== undefined && (
                      <div>
                        <p className="text-xs text-slate-500">
                          Rows
                        </p>

                        <p className="mt-1 text-xl font-bold text-blue-400">
                          {analyticsResult.rows.toLocaleString()}
                        </p>
                      </div>
                    )}


                    {analyticsResult.columns !== undefined && (
                      <div>
                        <p className="text-xs text-slate-500">
                          Columns
                        </p>

                        <p className="mt-1 text-xl font-bold text-blue-400">
                          {analyticsResult.columns}
                        </p>
                      </div>
                    )}
                  </>
                )}

              </div>

            </div>
          )}


          {/* AI Answer */}
          <div className="mt-6 rounded-lg border border-slate-800 bg-slate-950 p-5 text-slate-300">

            {loading && (
              <p className="text-blue-400">
                Analyzing your dataset...
              </p>
            )}


            {!loading && answer && (
              <p className="whitespace-pre-wrap">
                {answer}
              </p>
            )}


            {!loading && !answer && (
              <p className="text-slate-500">
                Your AI-generated analysis will appear here.
              </p>
            )}

          </div>

        </section>

      </main>


      {/* Footer */}
      <footer className="mt-12 border-t border-slate-800">

        <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-3 px-8 py-6 text-sm text-slate-500 md:flex-row">

          <p>
            © 2026 InsightFlow AI
          </p>

          <p>
            Built with React • FastAPI • RAG • LLM
          </p>

        </div>

      </footer>

    </div>
  );
}

export default App;