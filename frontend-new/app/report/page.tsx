"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import dynamic from "next/dynamic";
import Link from "next/link";

const ReactECharts = dynamic(() => import("echarts-for-react"), {
  ssr: false,
});

type AnalyticsResponse = {
  status: string;
  query: string;

  analytics: {
    customers?: {
      data?: {
        total_customers: number;
        active_customers: number;
        inactive_customers: number;
        male_customers?: number;
        female_customers?: number;
        other_customers?: number;
        average_annual_income?: number;
        total_occupations?: number;
      };
    };

    accounts?: {
      data?: {
        total_accounts: number;
        active_accounts: number;
        closed_accounts: number;
        total_balance: number;
        average_balance: number;
      };
    };

    transactions?: {
      data?: {
        total_transactions: number;
        completed_transactions: number;
        unsuccessful_transactions: number;
        total_transaction_amount: number;
        average_transaction_amount: number;
        transaction_types: {
          transaction_type: string;
          transaction_count: number;
        }[];
      };
    };

    cards?: {
      data?: {
        total_cards: number;
        active_cards: number;
        inactive_cards: number;
        credit_cards: number;
        debit_cards: number;
        total_credit_limit: number;
        total_available_limit: number;
        utilized_credit_limit: number;
        utilization_percentage: number;
        card_status_distribution: {
          status: string;
          count: number;
        }[];
        card_type_distribution: {
          card_type: string;
          count: number;
        }[];
        credit_limit_metrics: {
          metric: string;
          value: number;
        }[];
      };
    };

    fund_transfers?: {
      data?: {
        total_transfers: number;
        completed_transfers: number;
        unsuccessful_transfers: number;
        total_transfer_amount: number;
        average_transfer_amount: number;
        total_transfer_types?: number;
      };
    };

    complaints?: {
      data?: {
        total_complaints: number;
        open_complaints: number;
        resolved_complaints: number;
        high_priority_complaints: number;
        medium_priority_complaints: number;
        low_priority_complaints: number;
        total_complaint_types?: number;
      };
    };

    credit_scores?: {
      data?: {
        total_credit_scores: number;
        average_credit_score: number;
        highest_credit_score: number;
        lowest_credit_score: number;
        excellent_scores: number;
        good_scores: number;
        fair_scores: number;
        poor_scores: number;
        customers_with_credit_score?: number;
      };
    };

    card_transactions?: {
      data?: {
        total_card_transactions: number;
        completed_transactions: number;
        unsuccessful_transactions: number;
        total_transaction_amount: number;
        average_transaction_amount: number;
        total_merchants?: number;
        total_transaction_types?: number;
      };
    };

    loan_payments?: {
      data?: {
        total_payments: number;
        completed_payments: number;
        unsuccessful_payments: number;
        total_payment_amount: number;
        total_principal_paid: number;
        total_interest_paid: number;
        average_payment_amount: number;
        total_payment_methods?: number;
      };
    };

    loans?: {
      data?: {
        total_loans: number;
        active_loans: number;
        inactive_loans: number;
        total_loan_amount: number;
        total_outstanding_amount: number;
        average_interest_rate: number;
      };
    };

    branch_transactions?: {
      data?: {
        branch_id: number;
        branch_name: string;
        transaction_count: number;
        total_transaction_amount: number;
        average_transaction_amount: number;
      }[];
    };
  };

result?: {
  intent?: {
    domain: string;
    operation: string;
    requested_entities: string[];
    requested_metrics: string[];
  };

  kpis?: {
    label: string;
    value: string;
    unit: string;
    source_field: string;
  }[];

  charts?: {
    type: "bar" | "line" | "pie" | "donut";
    title: string;
    description: string;
    x_axis: string;
    y_axis: string;
    data: {
      label: string;
      value: number;
    }[];
  }[];

  table?: {
    title: string;
    columns: string[];
    rows: {
      values: string[];
    }[];
  };

  analysis?: {
    summary: string;
    insights: string[];
    risks: string[];
    opportunities: string[];
    recommendations: string[];
  };
};
};
const formatMoney = (value?: number) => {
  if (value === undefined || value === null || !Number.isFinite(value)) return "$0";

  if (Math.abs(value) >= 1_000_000_000) {
    return `$${(value / 1_000_000_000).toFixed(2)}B`;
  }

  if (Math.abs(value) >= 1_000_000) {
    return `$${(value / 1_000_000).toFixed(2)}M`;
  }

  if (Math.abs(value) >= 1_000) {
    return `$${(value / 1_000).toFixed(1)}K`;
  }

  return `$${value.toLocaleString(undefined, { minimumFractionDigits: 0, maximumFractionDigits: 2 })}`;
};

const chartBase = {
  backgroundColor: "transparent",
  textStyle: {
    color: "#c4b5fd",
    fontFamily: "inherit",
  },
};

export default function ReportPage() {
  const [data, setData] = useState<AnalyticsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [pdfLoading,setPdfLoading]=useState(false);
  const requestIdRef = useRef(0);

  const downloadPDF = async () => {
  if (!query.trim()) return;

  try {
    setPdfLoading(true);

    const response = await fetch(
      "http://127.0.0.1:8000/analytics/ai-report/pdf",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query,
        }),
      }
    );

    if (!response.ok) {
      throw new Error("Failed to generate PDF");
    }

    const blob = await response.blob();

    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = "banking_ai_report.pdf";

    document.body.appendChild(link);
    link.click();
    link.remove();

    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error("PDF download error:", error);
    alert("Failed to generate PDF. Please try again.");
  } finally {
    setPdfLoading(false);
  }
};

  const [query, setQuery] = useState(() => {
  if (typeof window !== "undefined") {
    return (
      new URLSearchParams(window.location.search).get("query") ||
      "Analyze customer activity and inactive customers"
    );
  }

  return "Analyze customer activity and inactive customers";
});

useEffect(() => {
  const syncQueryFromUrl = () => {
    const urlQuery =
      new URLSearchParams(window.location.search).get("query") ||
      "Analyze customer activity and inactive customers";

    setQuery((currentQuery) =>
      currentQuery === urlQuery ? currentQuery : urlQuery
    );
  };

  syncQueryFromUrl();

  const interval = setInterval(syncQueryFromUrl, 100);

  return () => clearInterval(interval);
}, []);

useEffect(() => {
  const requestId = ++requestIdRef.current;
  const controller = new AbortController();

  const loadReport = async () => {
    try {
      setLoading(true);
      setError("");
      setData(null);

      const response = await fetch(
        "http://127.0.0.1:8000/analytics/ai-report/query",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            query,
          }),
          signal: controller.signal,
        }
      );

      if (!response.ok) {
        throw new Error(`Backend returned ${response.status}`);
      }

      const result: AnalyticsResponse = await response.json();

      // Ignore any response belonging to an older request.
      if (requestId !== requestIdRef.current) {
        return;
      }

      setData(result);
      setLoading(false);
    } catch (err) {
      if (err instanceof DOMException && err.name === "AbortError") {
        return;
      }

      if (requestId !== requestIdRef.current) {
        return;
      }

      console.error(err);
      setError(
        "Unable to load analytics data. Please ensure the FastAPI backend is running on port 8000."
      );
      setLoading(false);
    }
  };

  loadReport();

  return () => {
    controller.abort();
  };
}, [query]);

  const queryLower = query.toLowerCase();

/*
 * CENTRAL QUERY ROUTING
 * Only ONE primary domain is selected for a query.
 * This prevents generic words such as "transaction", "risk",
 * "payment", etc. from overriding the actual business domain.
 */

const queryRoute = useMemo(() => {
  const q = queryLower;

  // 1. Branch analytics has highest priority for branch questions
  if (
    q.includes("branch") ||
    q.includes("branches") ||
    q.includes("branch-wise") ||
    q.includes("branch wise")
  ) {
    return "branch";
  }

  // 2. Loan analytics
  if (
    q.includes("loan") ||
    q.includes("loans") ||
    q.includes("repayment") ||
    q.includes("repay") ||
    q.includes("borrow") ||
    q.includes("borrowing") ||
    q.includes("interest rate") ||
    q.includes("outstanding loan") ||
    q.includes("loan performance")
  ) {
    return "loan";
  }

  // 3. Credit score analytics
  if (
    q.includes("credit score") ||
    q.includes("credit-score") ||
    q.includes("cibil") ||
    q.includes("fico") ||
    q.includes("credit rating")
  ) {
    return "credit";
  }

  // 4. Card analytics
  if (
    q.includes("card") ||
    q.includes("credit card") ||
    q.includes("debit card") ||
    q.includes("card utilization") ||
    q.includes("credit limit")
  ) {
    return "card";
  }

  // 5. Complaint analytics
  if (
    q.includes("complaint") ||
    q.includes("complaints") ||
    q.includes("support ticket") ||
    q.includes("customer issue") ||
    q.includes("service issue")
  ) {
    return "complaint";
  }

  // 6. Fund transfer analytics
  if (
    q.includes("fund transfer") ||
    q.includes("fund transfers") ||
    q.includes("wire transfer") ||
    q.includes("remittance")
  ) {
    return "fund_transfer";
  }

  // 7. Account analytics
  if (
    q.includes("account") ||
    q.includes("accounts") ||
    q.includes("account balance") ||
    q.includes("deposit account")
  ) {
    return "account";
  }

  // 8. Customer analytics
  if (
    q.includes("customer") ||
    q.includes("customers") ||
    q.includes("customer base") ||
    q.includes("occupation") ||
    q.includes("gender") ||
    q.includes("annual income") ||
    q.includes("inactive customers") ||
    q.includes("active customers")
  ) {
    return "customer";
  }

  // 9. Loan payment analytics
  if (
    q.includes("loan payment") ||
    q.includes("loan payments") ||
    q.includes("payment amount") ||
    q.includes("principal paid") ||
    q.includes("interest paid")
  ) {
    return "loan_payment";
  }

  // 10. Card transaction analytics
  if (
    q.includes("card transaction") ||
    q.includes("card transactions") ||
    q.includes("merchant transaction") ||
    q.includes("merchant")
  ) {
    return "card_transaction";
  }

  // 11. Generic transaction analytics
  if (
    q.includes("transaction") ||
    q.includes("transactions") ||
    q.includes("transaction volume") ||
    q.includes("transaction activity") ||
    q.includes("transaction amount")
  ) {
    return "transaction";
  }

  // 12. No specific domain
  return "overview";
}, [queryLower]);

const isBranchQuery = queryRoute === "branch";
const isLoanQuery = queryRoute === "loan";
const isCreditScoreQuery = queryRoute === "credit";
const isCardQuery = queryRoute === "card";
const isComplaintQuery = queryRoute === "complaint";
const isFundTransferQuery = queryRoute === "fund_transfer";
const isAccountQuery = queryRoute === "account";
const isCustomerQuery = queryRoute === "customer";
const isLoanPaymentQuery = queryRoute === "loan_payment";
const isCardTransactionQuery = queryRoute === "card_transaction";
const isTransactionQuery = queryRoute === "transaction";

  // Data extraction
  const customerData = data?.analytics?.customers?.data;
  const transactionData = data?.analytics?.transactions?.data;
  const cardData = data?.analytics?.cards?.data;
  const branchData = data?.analytics?.branch_transactions?.data;
  console.log("REPORT RESPONSE:", data);
  console.log("QUERY ROUTE:", queryRoute);
  console.log("CARD DATA:", data?.analytics?.cards);
  const accountData = data?.analytics?.accounts?.data;
  const loanData = data?.analytics?.loans?.data;
  const creditData = data?.analytics?.credit_scores?.data;
  const complaintData = data?.analytics?.complaints?.data;
  const fundTransferData = data?.analytics?.fund_transfers?.data;
  const aiVisualization = data?.result?.charts?.[0];

const aiTable = data?.result?.table;

const hasAIVisualization =
  !!aiVisualization &&
  Array.isArray(aiVisualization.data) &&
  aiVisualization.data.length > 0;

const hasAITable =
  !!aiTable &&
  Array.isArray(aiTable.rows) &&
  aiTable.rows.length > 0;

const hasAIQueryResult = hasAIVisualization || hasAITable;

  // Active domain identification
  const activeDomain = useMemo(() => {
    if (isCustomerQuery && customerData) return "Customer Intelligence";
    if(isBranchQuery && branchData) return "Branch Transaction Analytics";
    if (isCardQuery && cardData) return "Card Portfolio Analytics";
    if (isTransactionQuery && transactionData) return "Transaction Performance";
    if (isAccountQuery && accountData) return "Account Analytics";
    if (isLoanQuery && loanData) return "Loan Portfolio Analytics";
    if (isCreditScoreQuery && creditData) return "Credit Score Intelligence";
    if (isComplaintQuery && complaintData) return "Complaint & Support Analytics";
    if (isFundTransferQuery && fundTransferData) return "Fund Transfer Intelligence";
    return "Banking Overview";
  }, [
    isBranchQuery,
    isCustomerQuery,
    customerData,
    isCardQuery,
    cardData,
    isTransactionQuery,
    transactionData,
    isAccountQuery,
    accountData,
    isLoanQuery,
    loanData,
    isCreditScoreQuery,
    creditData,
    isComplaintQuery,
    complaintData,
    isFundTransferQuery,
    fundTransferData,
  ]);

  const aiVisualizationOption = useMemo(() => {
  if (!aiVisualization || !hasAIVisualization) return {};

  const labels = aiVisualization.data.map((item) => item.label);
  const values = aiVisualization.data.map((item) => item.value);

  const commonTooltip = {
    backgroundColor: "#170d29",
    borderColor: "#8b5cf6",
    textStyle: { color: "#ffffff" },
  };

  if (
    aiVisualization.type === "pie" ||
    aiVisualization.type === "donut"
  ) {
    return {
      ...chartBase,
      tooltip: {
        trigger: "item",
        ...commonTooltip,
        formatter: "{b}: <b>{c}</b> ({d}%)",
      },
      legend: {
        bottom: 0,
        textStyle: { color: "#c4b5fd" },
      },
      series: [
        {
          name: aiVisualization.y_axis || "Value",
          type: "pie",
          radius:
            aiVisualization.type === "donut"
              ? ["48%", "72%"]
              : "65%",
          center: ["50%", "45%"],
          data: aiVisualization.data.map((item) => ({
            name: item.label,
            value: item.value,
          })),
          label: {
            color: "#ffffff",
          },
        },
      ],
    };
  }

  return {
    ...chartBase,
    tooltip: {
      trigger: "axis",
      axisPointer: {
        type: "shadow",
      },
      ...commonTooltip,
    },
    grid: {
      left: 65,
      right: 30,
      top: 45,
      bottom: 75,
      containLabel: true,
    },
    xAxis: {
      type: "category",
      name: aiVisualization.x_axis || "",
      data: labels,
      axisLabel: {
        color: "#c4b5fd",
        rotate: labels.length > 6 ? 30 : 0,
        fontSize: 11,
      },
      axisLine: {
        lineStyle: {
          color: "rgba(167,139,250,0.25)",
        },
      },
    },
    yAxis: {
      type: "value",
      name: aiVisualization.y_axis || "",
      nameTextStyle: {
        color: "#8f82a8",
      },
      axisLabel: {
        color: "#a78bfa",
      },
      splitLine: {
        lineStyle: {
          color: "rgba(139,92,246,0.10)",
        },
      },
    },
    series: [
      {
        name: aiVisualization.y_axis || "Value",
        type:
          aiVisualization.type === "line"
            ? "line"
            : "bar",
        data: values,
        smooth: aiVisualization.type === "line",
        barMaxWidth: 45,
        itemStyle: {
          color: "#8b5cf6",
          borderRadius:
            aiVisualization.type === "bar"
              ? [8, 8, 0, 0]
              : undefined,
        },
        lineStyle:
          aiVisualization.type === "line"
            ? {
                color: "#8b5cf6",
                width: 3,
              }
            : undefined,
      },
    ],
  };
}, [aiVisualization, hasAIVisualization]);

  /*
   * ---------------------------------------------------------
   * CUSTOMER CHARTS
   * ---------------------------------------------------------
   */

  const customerActivityRate =
    customerData && customerData.total_customers > 0
      ? (customerData.active_customers / customerData.total_customers) * 100
      : 0;

  const customerStatusDonutOption = useMemo(() => {
    if (!customerData) return {};

    const active = customerData.active_customers || 0;
    const inactive = customerData.inactive_customers || 0;

    return {
      ...chartBase,
      tooltip: {
        trigger: "item",
        backgroundColor: "#170d29",
        borderColor: "#a855f7",
        textStyle: { color: "#ffffff" },
        formatter: "{b}: <b>{c}</b> ({d}%)",
      },
      legend: {
        bottom: 0,
        textStyle: { color: "#c4b5fd" },
      },
      series: [
        {
          name: "Customer Status",
          type: "pie",
          radius: ["54%", "76%"],
          center: ["50%", "45%"],
          avoidLabelOverlap: true,
          itemStyle: {
            borderColor: "#0b0614",
            borderWidth: 3,
          },
          label: {
            show: true,
            position: "center",
            formatter: () => `{rate|${customerActivityRate.toFixed(1)}%}\n{label|Active Rate}`,
            rich: {
              rate: {
                fontSize: 22,
                fontWeight: "bold",
                color: "#ffffff",
                lineHeight: 28,
              },
              label: {
                fontSize: 11,
                color: "#a78bfa",
                lineHeight: 16,
              },
            },
          },
          data: [
            {
              value: active,
              name: "Active Customers",
              itemStyle: { color: "#8b5cf6" },
            },
            {
              value: inactive,
              name: "Inactive Customers",
              itemStyle: { color: "#ef4444" },
            },
          ],
        },
      ],
    };
  }, [customerData, customerActivityRate]);

  const customerActivityBarOption = useMemo(() => {
    if (!customerData) return {};

    const categories = [
      "Total",
      "Active",
      "Inactive",
      "Male",
      "Female",
      "Other",
    ];

    const values = [
      { val: customerData.total_customers, color: "#8b5cf6" },
      { val: customerData.active_customers, color: "#22d3ee" },
      { val: customerData.inactive_customers, color: "#ef4444" },
      { val: customerData.male_customers || 0, color: "#7c3aed" },
      { val: customerData.female_customers || 0, color: "#38bdf8" },
      { val: customerData.other_customers || 0, color: "#c084fc" },
    ];

    return {
      ...chartBase,
      tooltip: {
        trigger: "axis",
        backgroundColor: "#170d29",
        borderColor: "#a855f7",
        textStyle: { color: "#ffffff" },
      },
      grid: {
        left: 55,
        right: 25,
        top: 30,
        bottom: 45,
      },
      xAxis: {
        type: "category",
        data: categories,
        axisLabel: {
          color: "#c4b5fd",
          fontSize: 11,
        },
        axisLine: {
          lineStyle: { color: "#31204f" },
        },
      },
      yAxis: {
        type: "value",
        axisLabel: { color: "#a78bfa" },
        splitLine: {
          lineStyle: { color: "rgba(139,92,246,0.10)" },
        },
      },
      series: [
        {
          name: "Customers",
          type: "bar",
          barWidth: "44%",
          data: values.map((item) => ({
            value: item.val,
            itemStyle: {
              color: item.color,
              borderRadius: [8, 8, 0, 0],
            },
          })),
        },
      ],
    };
  }, [customerData]);

  const customerGenderPieOption = useMemo(() => {
    if (!customerData) return {};

    return {
      ...chartBase,
      tooltip: {
        trigger: "item",
        backgroundColor: "#170d29",
        borderColor: "#a855f7",
        textStyle: { color: "#ffffff" },
        formatter: "{b}: <b>{c}</b> ({d}%)",
      },
      legend: {
        bottom: 0,
        textStyle: { color: "#c4b5fd" },
      },
      series: [
        {
          name: "Gender Demographics",
          type: "pie",
          radius: ["0%", "70%"],
          center: ["50%", "45%"],
          itemStyle: {
            borderColor: "#0b0614",
            borderWidth: 3,
          },
          label: {
            color: "#ffffff",
            formatter: "{b}\n{d}%",
          },
          data: [
            {
              value: customerData.male_customers || 0,
              name: "Male",
              itemStyle: { color: "#7c3aed" },
            },
            {
              value: customerData.female_customers || 0,
              name: "Female",
              itemStyle: { color: "#22d3ee" },
            },
            {
              value: customerData.other_customers || 0,
              name: "Other",
              itemStyle: { color: "#c084fc" },
            },
          ],
        },
      ],
    };
  }, [customerData]);

  /*
   * ---------------------------------------------------------
   * TRANSACTION CHARTS
   * ---------------------------------------------------------
   */

  const transactionSuccessRate = useMemo(() => {
    if (!transactionData?.total_transactions) return 0;
    const structuredReport = useMemo(() => {
  const raw = data?.result;

  if (!raw) return null;

  try {
    if (typeof raw === "object") return raw;

    const cleaned = String(raw)
      .replace(/^```json\s*/i, "")
      .replace(/^```\s*/i, "")
      .replace(/\s*```$/i, "")
      .trim();

    return JSON.parse(cleaned);
  } catch (error) {
    console.error("Unable to parse structured AI result:", error);
    return null;
  }
}, [data]);

const dynamicKpis = structuredReport?.kpis || [];
const dynamicCharts = structuredReport?.charts || [];
const dynamicTable = structuredReport?.table;
const dynamicAnalysis = structuredReport?.analysis;

return (
      (transactionData.completed_transactions /
        transactionData.total_transactions) *
      100
    );
  }, [transactionData]);

  const transactionStatusDonutOption = useMemo(() => {
    if (!transactionData) return {};

    return {
      ...chartBase,
      tooltip: {
        trigger: "item",
        backgroundColor: "#170d29",
        borderColor: "#6d28d9",
        textStyle: { color: "#ffffff" },
      },
      legend: {
        bottom: 0,
        textStyle: { color: "#c4b5fd" },
      },
      series: [
        {
          name: "Transaction Status",
          type: "pie",
          radius: ["54%", "76%"],
          center: ["50%", "45%"],
          avoidLabelOverlap: true,
          itemStyle: {
            borderColor: "#0b0614",
            borderWidth: 3,
          },
          label: {
            show: true,
            position: "center",
            formatter: () => `{rate|${transactionSuccessRate.toFixed(1)}%}\n{label|Success Rate}`,
            rich: {
              rate: {
                fontSize: 22,
                fontWeight: "bold",
                color: "#ffffff",
                lineHeight: 28,
              },
              label: {
                fontSize: 11,
                color: "#a78bfa",
                lineHeight: 16,
              },
            },
          },
          data: [
            {
              value: transactionData.completed_transactions,
              name: "Completed",
              itemStyle: { color: "#8b5cf6" },
            },
            {
              value: transactionData.unsuccessful_transactions,
              name: "Unsuccessful",
              itemStyle: { color: "#ef4444" },
            },
          ],
        },
      ],
    };
  }, [transactionData, transactionSuccessRate]);

  const transactionVolumeLineOption = useMemo(() => {
    if (!transactionData) return {};
    const types = transactionData.transaction_types || [];

    return {
      ...chartBase,
      tooltip: {
        trigger: "axis",
        backgroundColor: "#170d29",
        borderColor: "#6d28d9",
        textStyle: { color: "#ffffff" },
      },
      grid: {
        left: 45,
        right: 25,
        top: 30,
        bottom: 50,
      },
      xAxis: {
        type: "category",
        boundaryGap: false,
        data: types.map((item) => item.transaction_type),
        axisLabel: {
          color: "#a78bfa",
          rotate: 15,
        },
      },
      yAxis: {
        type: "value",
        axisLabel: { color: "#a78bfa" },
        splitLine: {
          lineStyle: { color: "rgba(139,92,246,0.10)" },
        },
      },
      series: [
        {
          name: "Transaction Count",
          type: "line",
          smooth: true,
          data: types.map((item) => item.transaction_count),
          symbol: "circle",
          symbolSize: 8,
          lineStyle: { width: 3.5, color: "#a78bfa" },
          itemStyle: { color: "#c4b5fd" },
          areaStyle: {
            color: {
              type: "linear",
              x: 0,
              y: 0,
              x2: 0,
              y2: 1,
              colorStops: [
                { offset: 0, color: "rgba(139,92,246,0.35)" },
                { offset: 1, color: "rgba(139,92,246,0.02)" },
              ],
            },
          },
        },
      ],
    };
  }, [transactionData]);

  const transactionTypeBarOption = useMemo(() => {
    if (!transactionData) return {};
    const types = transactionData.transaction_types || [];

    return {
      ...chartBase,
      tooltip: {
        trigger: "axis",
        backgroundColor: "#170d29",
        borderColor: "#6d28d9",
        textStyle: { color: "#ffffff" },
      },
      grid: {
        left: 45,
        right: 25,
        top: 30,
        bottom: 50,
      },
      xAxis: {
        type: "category",
        data: types.map((item) => item.transaction_type),
        axisLabel: {
          color: "#a78bfa",
          rotate: 15,
        },
        axisLine: {
          lineStyle: { color: "#31204f" },
        },
      },
      yAxis: {
        type: "value",
        axisLabel: { color: "#a78bfa" },
        splitLine: {
          lineStyle: { color: "rgba(139,92,246,0.10)" },
        },
      },
      series: [
        {
          name: "Volume",
          type: "bar",
          barWidth: "45%",
          data: types.map((item) => item.transaction_count),
          itemStyle: {
            color: "#8b5cf6",
            borderRadius: [8, 8, 0, 0],
          },
        },
      ],
    };
  }, [transactionData]);

  /*
   * ---------------------------------------------------------
   * CARD CHARTS
   * ---------------------------------------------------------
   */

  const cardStatusDonutOption = useMemo(() => {
    if (!cardData) return {};

    return {
      ...chartBase,
      tooltip: {
        trigger: "item",
        backgroundColor: "#170d29",
        borderColor: "#6d28d9",
        textStyle: { color: "#ffffff" },
      },
      legend: {
        bottom: 0,
        textStyle: { color: "#c4b5fd" },
      },
      series: [
        {
          name: "Card Status",
          type: "pie",
          radius: ["50%", "74%"],
          center: ["50%", "45%"],
          itemStyle: {
            borderColor: "#0b0614",
            borderWidth: 3,
          },
          label: {
            color: "#ffffff",
            formatter: "{b}\n{d}%",
          },
          data: cardData.card_status_distribution.map((item) => ({
            name: item.status,
            value: item.count,
          })),
        },
      ],
    };
  }, [cardData]);

  const cardCreditLimitBarOption = useMemo(() => {
    if (!cardData) return {};

    return {
      ...chartBase,
      tooltip: {
        trigger: "axis",
        backgroundColor: "#170d29",
        borderColor: "#6d28d9",
        textStyle: { color: "#ffffff" },
        formatter: (params: any) => {
          const item = params[0];
          return `${item.name}<br/><b>${formatMoney(item.value)}</b>`;
        },
      },
      grid: {
        left: 60,
        right: 25,
        top: 30,
        bottom: 45,
      },
      xAxis: {
        type: "category",
        data: cardData.credit_limit_metrics.map((item) => item.metric),
        axisLabel: { color: "#c4b5fd", rotate: 12 },
      },
      yAxis: {
        type: "value",
        axisLabel: {
          color: "#a78bfa",
          formatter: (val: number) => formatMoney(val),
        },
        splitLine: {
          lineStyle: { color: "rgba(139,92,246,0.10)" },
        },
      },
      series: [
        {
          type: "bar",
          barWidth: "42%",
          data: cardData.credit_limit_metrics.map((item, index) => ({
            value: item.value,
            itemStyle: {
              color:
                index === 0
                  ? "#7c3aed"
                  : index === 1
                  ? "#22d3ee"
                  : "#c084fc",
              borderRadius: [8, 8, 0, 0],
            },
          })),
        },
      ],
    };
  }, [cardData]);

  const cardTypePieOption = useMemo(() => {
    if (!cardData) return {};

    return {
      ...chartBase,
      tooltip: {
        trigger: "item",
        backgroundColor: "#170d29",
        borderColor: "#6d28d9",
        textStyle: { color: "#ffffff" },
      },
      legend: {
        bottom: 0,
        textStyle: { color: "#c4b5fd" },
      },
      series: [
        {
          type: "pie",
          radius: ["0%", "68%"],
          center: ["50%", "45%"],
          itemStyle: {
            borderColor: "#0b0614",
            borderWidth: 3,
          },
          label: {
            color: "#ffffff",
            formatter: "{b}\n{d}%",
          },
          data: cardData.card_type_distribution.map((item, i) => ({
            name: item.card_type,
            value: item.count,
            itemStyle: {
              color: i === 0 ? "#8b5cf6" : "#22d3ee",
            },
          })),
        },
      ],
    };
  }, [cardData]);

  /*
   * ---------------------------------------------------------
   * ACCOUNT CHARTS
   * ---------------------------------------------------------
   */

  const accountStatusDonutOption = useMemo(() => {
    if (!accountData) return {};
    return {
      ...chartBase,
      tooltip: {
        trigger: "item",
        backgroundColor: "#170d29",
        borderColor: "#6d28d9",
        textStyle: { color: "#ffffff" },
      },
      legend: { bottom: 0, textStyle: { color: "#c4b5fd" } },
      series: [
        {
          name: "Account Status",
          type: "pie",
          radius: ["50%", "74%"],
          center: ["50%", "45%"],
          avoidLabelOverlap: true,
          itemStyle: { borderColor: "#0b0614", borderWidth: 3 },
          label: { color: "#ffffff", formatter: "{b}\n{d}%" },
          data: [
            {
              value: accountData.active_accounts,
              name: "Active Accounts",
              itemStyle: { color: "#8b5cf6" },
            },
            {
              value: accountData.closed_accounts,
              name: "Closed Accounts",
              itemStyle: { color: "#ef4444" },
            },
          ],
        },
      ],
    };
  }, [accountData]);

  const accountBalanceBarOption = useMemo(() => {
    if (!accountData) return {};
    return {
      ...chartBase,
      tooltip: {
        trigger: "axis",
        backgroundColor: "#170d29",
        borderColor: "#6d28d9",
        textStyle: { color: "#ffffff" },
        formatter: (params: any) =>
          `${params[0].name}: <b>${formatMoney(params[0].value)}</b>`,
      },
      grid: { left: 60, right: 25, top: 30, bottom: 45 },
      xAxis: {
        type: "category",
        data: ["Total Balance", "Average Balance"],
        axisLabel: { color: "#c4b5fd" },
      },
      yAxis: {
        type: "value",
        axisLabel: {
          color: "#a78bfa",
          formatter: (v: number) => formatMoney(v),
        },
        splitLine: { lineStyle: { color: "rgba(139,92,246,0.10)" } },
      },
      series: [
        {
          type: "bar",
          barWidth: "40%",
          data: [
            {
              value: accountData.total_balance,
              itemStyle: { color: "#7c3aed", borderRadius: [8, 8, 0, 0] },
            },
            {
              value: accountData.average_balance,
              itemStyle: { color: "#22d3ee", borderRadius: [8, 8, 0, 0] },
            },
          ],
        },
      ],
    };
  }, [accountData]);

  /*
   * ---------------------------------------------------------
   * LOAN CHARTS
   * ---------------------------------------------------------
   */

  const loanStatusDonutOption = useMemo(() => {
    if (!loanData) return {};
    return {
      ...chartBase,
      tooltip: {
        trigger: "item",
        backgroundColor: "#170d29",
        borderColor: "#6d28d9",
        textStyle: { color: "#ffffff" },
      },
      legend: { bottom: 0, textStyle: { color: "#c4b5fd" } },
      series: [
        {
          name: "Loan Status",
          type: "pie",
          radius: ["50%", "74%"],
          center: ["50%", "45%"],
          avoidLabelOverlap: true,
          itemStyle: { borderColor: "#0b0614", borderWidth: 3 },
          label: { color: "#ffffff", formatter: "{b}\n{d}%" },
          data: [
            {
              value: loanData.active_loans,
              name: "Active Loans",
              itemStyle: { color: "#8b5cf6" },
            },
            {
              value: loanData.inactive_loans,
              name: "Closed / Inactive",
              itemStyle: { color: "#22d3ee" },
            },
          ],
        },
      ],
    };
  }, [loanData]);

  const loanAmountBarOption = useMemo(() => {
    if (!loanData) return {};
    return {
      ...chartBase,
      tooltip: {
        trigger: "axis",
        backgroundColor: "#170d29",
        borderColor: "#6d28d9",
        textStyle: { color: "#ffffff" },
        formatter: (params: any) =>
          `${params[0].name}: <b>${formatMoney(params[0].value)}</b>`,
      },
      grid: { left: 60, right: 25, top: 30, bottom: 45 },
      xAxis: {
        type: "category",
        data: ["Total Loan Amount", "Outstanding Amount"],
        axisLabel: { color: "#c4b5fd" },
      },
      yAxis: {
        type: "value",
        axisLabel: {
          color: "#a78bfa",
          formatter: (v: number) => formatMoney(v),
        },
        splitLine: { lineStyle: { color: "rgba(139,92,246,0.10)" } },
      },
      series: [
        {
          type: "bar",
          barWidth: "40%",
          data: [
            {
              value: loanData.total_loan_amount,
              itemStyle: { color: "#7c3aed", borderRadius: [8, 8, 0, 0] },
            },
            {
              value: loanData.total_outstanding_amount,
              itemStyle: { color: "#ef4444", borderRadius: [8, 8, 0, 0] },
            },
          ],
        },
      ],
    };
  }, [loanData]);

  /*
   * ---------------------------------------------------------
   * CREDIT SCORE CHARTS
   * ---------------------------------------------------------
   */

  const creditScoreTierDonutOption = useMemo(() => {
    if (!creditData) return {};
    return {
      ...chartBase,
      tooltip: {
        trigger: "item",
        backgroundColor: "#170d29",
        borderColor: "#6d28d9",
        textStyle: { color: "#ffffff" },
      },
      legend: { bottom: 0, textStyle: { color: "#c4b5fd" } },
      series: [
        {
          name: "Score Tiers",
          type: "pie",
          radius: ["48%", "72%"],
          center: ["50%", "45%"],
          itemStyle: { borderColor: "#0b0614", borderWidth: 3 },
          label: { color: "#ffffff", formatter: "{b}\n{d}%" },
          data: [
            {
              value: creditData.excellent_scores,
              name: "Excellent",
              itemStyle: { color: "#22c55e" },
            },
            {
              value: creditData.good_scores,
              name: "Good",
              itemStyle: { color: "#3b82f6" },
            },
            {
              value: creditData.fair_scores,
              name: "Fair",
              itemStyle: { color: "#f59e0b" },
            },
            {
              value: creditData.poor_scores,
              name: "Poor",
              itemStyle: { color: "#ef4444" },
            },
          ],
        },
      ],
    };
  }, [creditData]);

  const creditScoreBarOption = useMemo(() => {
    if (!creditData) return {};
    return {
      ...chartBase,
      tooltip: {
        trigger: "axis",
        backgroundColor: "#170d29",
        borderColor: "#6d28d9",
        textStyle: { color: "#ffffff" },
      },
      grid: { left: 45, right: 25, top: 30, bottom: 45 },
      xAxis: {
        type: "category",
        data: ["Excellent", "Good", "Fair", "Poor"],
        axisLabel: { color: "#c4b5fd" },
      },
      yAxis: {
        type: "value",
        axisLabel: { color: "#a78bfa" },
        splitLine: { lineStyle: { color: "rgba(139,92,246,0.10)" } },
      },
      series: [
        {
          type: "bar",
          barWidth: "42%",
          data: [
            { value: creditData.excellent_scores, itemStyle: { color: "#22c55e", borderRadius: [8, 8, 0, 0] } },
            { value: creditData.good_scores, itemStyle: { color: "#3b82f6", borderRadius: [8, 8, 0, 0] } },
            { value: creditData.fair_scores, itemStyle: { color: "#f59e0b", borderRadius: [8, 8, 0, 0] } },
            { value: creditData.poor_scores, itemStyle: { color: "#ef4444", borderRadius: [8, 8, 0, 0] } },
          ],
        },
      ],
    };
  }, [creditData]);

  /*
   * ---------------------------------------------------------
   * COMPLAINT & TRANSFER CHARTS
   * ---------------------------------------------------------
   */

  const complaintStatusDonutOption = useMemo(() => {
    if (!complaintData) return {};
    return {
      ...chartBase,
      tooltip: {
        trigger: "item",
        backgroundColor: "#170d29",
        borderColor: "#6d28d9",
        textStyle: { color: "#ffffff" },
      },
      legend: { bottom: 0, textStyle: { color: "#c4b5fd" } },
      series: [
        {
          name: "Complaint Status",
          type: "pie",
          radius: ["50%", "74%"],
          center: ["50%", "45%"],
          itemStyle: { borderColor: "#0b0614", borderWidth: 3 },
          label: { color: "#ffffff", formatter: "{b}\n{d}%" },
          data: [
            {
              value: complaintData.resolved_complaints,
              name: "Resolved",
              itemStyle: { color: "#22c55e" },
            },
            {
              value: complaintData.open_complaints,
              name: "Open",
              itemStyle: { color: "#ef4444" },
            },
          ],
        },
      ],
    };
  }, [complaintData]);

  const complaintPriorityPieOption = useMemo(() => {
    if (!complaintData) return {};
    return {
      ...chartBase,
      tooltip: {
        trigger: "item",
        backgroundColor: "#170d29",
        borderColor: "#6d28d9",
        textStyle: { color: "#ffffff" },
      },
      legend: { bottom: 0, textStyle: { color: "#c4b5fd" } },
      series: [
        {
          name: "Priority",
          type: "pie",
          radius: ["0%", "68%"],
          center: ["50%", "45%"],
          itemStyle: { borderColor: "#0b0614", borderWidth: 3 },
          label: { color: "#ffffff", formatter: "{b}\n{d}%" },
          data: [
            {
              value: complaintData.high_priority_complaints,
              name: "High Priority",
              itemStyle: { color: "#ef4444" },
            },
            {
              value: complaintData.medium_priority_complaints,
              name: "Medium Priority",
              itemStyle: { color: "#f59e0b" },
            },
            {
              value: complaintData.low_priority_complaints,
              name: "Low Priority",
              itemStyle: { color: "#3b82f6" },
            },
          ],
        },
      ],
    };
  }, [complaintData]);

  const fundTransferStatusOption = useMemo(() => {
    if (!fundTransferData) return {};
    return {
      ...chartBase,
      tooltip: {
        trigger: "item",
        backgroundColor: "#170d29",
        borderColor: "#6d28d9",
        textStyle: { color: "#ffffff" },
      },
      legend: { bottom: 0, textStyle: { color: "#c4b5fd" } },
      series: [
        {
          name: "Transfer Status",
          type: "pie",
          radius: ["50%", "74%"],
          center: ["50%", "45%"],
          itemStyle: { borderColor: "#0b0614", borderWidth: 3 },
          label: { color: "#ffffff", formatter: "{b}\n{d}%" },
          data: [
            {
              value: fundTransferData.completed_transfers,
              name: "Completed",
              itemStyle: { color: "#8b5cf6" },
            },
            {
              value: fundTransferData.unsuccessful_transfers,
              name: "Unsuccessful",
              itemStyle: { color: "#ef4444" },
            },
          ],
        },
      ],
    };
  }, [fundTransferData]);

  /*
   * ---------------------------------------------------------
   * LOADING STATE
   * ---------------------------------------------------------
   */

  if (loading || !data || data.query !== query) {
    const structuredReport = useMemo(() => {
  const raw = data?.result;

  if (!raw) return null;

  try {
    if (typeof raw === "object") return raw;

    const cleaned = String(raw)
      .replace(/^```json\s*/i, "")
      .replace(/^```\s*/i, "")
      .replace(/\s*```$/i, "")
      .trim();

    return JSON.parse(cleaned);
  } catch (error) {
    console.error("Unable to parse structured AI result:", error);
    return null;
  }
}, [data]);

const dynamicKpis = structuredReport?.kpis || [];
const dynamicCharts = structuredReport?.charts || [];
const dynamicTable = structuredReport?.table;
const dynamicAnalysis = structuredReport?.analysis;

return (
      <main className="premium-background">
        <div className="purple-glow purple-glow-one" />
        <div className="purple-glow purple-glow-two" />
        <div className="purple-glow purple-glow-three" />
        <div className="premium-grid" />

        <div
          style={{
            minHeight: "100vh",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            color: "#ddd6fe",
            fontSize: 18,
            gap: 16,
          }}
        >
          <div
            style={{
              width: 46,
              height: 46,
              borderRadius: "50%",
              border: "3px solid rgba(139,92,246,0.2)",
              borderTopColor: "#8b5cf6",
              animation: "spin 1s linear infinite",
            }}
          />
          <span style={{ fontWeight: 650, letterSpacing: "0.02em" }}>
            Generating Executive Analytics Dashboard...
          </span>
          <span style={{ fontSize: 13, color: "#a78bfa" }}>
            Extracting real-time banking metrics
          </span>
        </div>
      </main>
    );
  }

  if (error || !data) {
    const structuredReport = useMemo(() => {
  const raw = data?.result;

  if (!raw) return null;

  try {
    if (typeof raw === "object") return raw;

    const cleaned = String(raw)
      .replace(/^```json\s*/i, "")
      .replace(/^```\s*/i, "")
      .replace(/\s*```$/i, "")
      .trim();

    return JSON.parse(cleaned);
  } catch (error) {
    console.error("Unable to parse structured AI result:", error);
    return null;
  }
}, [data]);

const dynamicKpis = structuredReport?.kpis || [];
const dynamicCharts = structuredReport?.charts || [];
const dynamicTable = structuredReport?.table;
const dynamicAnalysis = structuredReport?.analysis;

return (
      <main className="premium-background">
        <div className="purple-glow purple-glow-one" />
        <div className="purple-glow purple-glow-two" />
        <div className="purple-glow purple-glow-three" />
        <div className="premium-grid" />

        <div
          style={{
            minHeight: "100vh",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            color: "#fca5a5",
            fontSize: 17,
            padding: 30,
            textAlign: "center",
            gap: 20,
          }}
        >
          <div
            style={{
              background: "rgba(239, 68, 68, 0.1)",
              border: "1px solid rgba(239, 68, 68, 0.25)",
              borderRadius: 16,
              padding: "24px 32px",
              maxWidth: 550,
            }}
          >
            <div style={{ fontSize: 24, marginBottom: 8 }}>âš ï¸</div>
            <h3 style={{ color: "#ffffff", margin: "0 0 8px" }}>
              Analytics Unavailable
            </h3>
            <p style={{ margin: 0, fontSize: 14, color: "#fca5a5" }}>
              {error || "No analytics data could be retrieved from the backend."}
            </p>
          </div>
          <Link
            href="/"
            style={{
              padding: "10px 22px",
              borderRadius: 12,
              background: "rgba(139,92,246,0.2)",
              border: "1px solid rgba(139,92,246,0.3)",
              color: "#ffffff",
              textDecoration: "none",
              fontSize: 14,
              fontWeight: 600,
            }}
          >
            â† Return to Search
          </Link>
        </div>
      </main>
    );
  }

  /*
   * ---------------------------------------------------------
   * REUSABLE UI COMPONENTS
   * ---------------------------------------------------------
   */

  const KPI = ({
    label,
    value,
    subtext,
    accent = "#8b5cf6",
  }: {
    label: string;
    value: string | number;
    subtext?: string;
    accent?: string;
  }) => (
    <div
      style={{
        background: "rgba(18, 11, 31, 0.78)",
        border: "1px solid rgba(139,92,246,0.18)",
        borderRadius: 16,
        padding: "18px 20px",
        boxShadow: "0 14px 40px rgba(0,0,0,0.22)",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
      }}
    >
      <div>
        <div
          style={{
            fontSize: 11,
            color: "#a78bfa",
            marginBottom: 6,
            textTransform: "uppercase",
            letterSpacing: "0.08em",
            fontWeight: 700,
          }}
        >
          {label}
        </div>

        <div
          style={{
            fontSize: 26,
            fontWeight: 750,
            color: "#ffffff",
            lineHeight: 1.1,
          }}
        >
          {typeof value === "number" ? value.toLocaleString() : value}
        </div>

        {subtext && (
          <div
            style={{
              fontSize: 11.5,
              color: "#8f82a8",
              marginTop: 5,
            }}
          >
            {subtext}
          </div>
        )}
      </div>

      <div
        style={{
          width: 32,
          height: 3,
          background: accent,
          borderRadius: 8,
          marginTop: 12,
        }}
      />
    </div>
  );

  const InsightCard = ({
    title,
    metric,
    subtext,
    badge,
    icon,
    accent = "#8b5cf6",
  }: {
    title: string;
    metric: string;
    subtext: string;
    badge?: string;
    icon?: string;
    accent?: string;
  }) => (
    <div
      style={{
        background: "rgba(18, 11, 31, 0.78)",
        border: "1px solid rgba(139,92,246,0.18)",
        borderRadius: 16,
        padding: "18px 20px",
        boxShadow: "0 14px 40px rgba(0,0,0,0.20)",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
      }}
    >
      <div>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            marginBottom: 8,
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
            {icon && <span style={{ fontSize: 13, color: accent }}>{icon}</span>}
            <span
              style={{
                fontSize: 11,
                fontWeight: 750,
                color: "#a78bfa",
                textTransform: "uppercase",
                letterSpacing: "0.08em",
              }}
            >
              {title}
            </span>
          </div>
          {badge && (
            <span
              style={{
                fontSize: 9.5,
                fontWeight: 750,
                padding: "2px 7px",
                borderRadius: 6,
                background: `${accent}20`,
                color: accent,
                border: `1px solid ${accent}40`,
                textTransform: "uppercase",
              }}
            >
              {badge}
            </span>
          )}
        </div>

        <div
          style={{
            fontSize: 17.5,
            fontWeight: 750,
            color: "#ffffff",
            margin: "3px 0 5px",
          }}
        >
          {metric}
        </div>

        <div
          style={{
            fontSize: 12.5,
            color: "#c4b5fd",
            lineHeight: 1.5,
          }}
        >
          {subtext}
        </div>
      </div>

      <div
        style={{
          width: 28,
          height: 2.5,
          background: accent,
          borderRadius: 6,
          marginTop: 12,
        }}
      />
    </div>
  );

  const ChartCard = ({
    title,
    subtitle,
    chartType,
    option,
    height = 320,
  }: {
    title: string;
    subtitle?: string;
    chartType?: string;
    option: any;
    height?: number;
  }) => (
    <div
      style={{
        background: "rgba(18, 11, 31, 0.76)",
        border: "1px solid rgba(139,92,246,0.17)",
        borderRadius: 20,
        padding: "20px 22px",
        boxShadow: "0 20px 60px rgba(0,0,0,0.24)",
        backdropFilter: "blur(18px)",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "flex-start",
          justifyContent: "space-between",
          marginBottom: 10,
        }}
      >
        <div>
          <h3
            style={{
              margin: 0,
              color: "#ffffff",
              fontSize: 16,
              fontWeight: 650,
            }}
          >
            {title}
          </h3>

          {subtitle && (
            <p
              style={{
                margin: "4px 0 0",
                color: "#8f82a8",
                fontSize: 12,
              }}
            >
              {subtitle}
            </p>
          )}
        </div>

        {chartType && (
          <span
            style={{
              fontSize: 10,
              fontWeight: 700,
              letterSpacing: "0.08em",
              textTransform: "uppercase",
              padding: "3px 9px",
              borderRadius: 8,
              background: "rgba(139,92,246,0.15)",
              border: "1px solid rgba(139,92,246,0.25)",
              color: "#c4b5fd",
            }}
          >
            {chartType}
          </span>
        )}
      </div>

      <ReactECharts
        option={option}
        style={{
          height,
          width: "100%",
        }}
        opts={{
          renderer: "canvas",
        }}
      />
    </div>
  );

  /*
   * ---------------------------------------------------------
   * DASHBOARD PAGE JSX
   * ---------------------------------------------------------
   */

  const structuredReport = useMemo(() => {
  const raw = data?.result;

  if (!raw) return null;

  try {
    if (typeof raw === "object") return raw;

    const cleaned = String(raw)
      .replace(/^```json\s*/i, "")
      .replace(/^```\s*/i, "")
      .replace(/\s*```$/i, "")
      .trim();

    return JSON.parse(cleaned);
  } catch (error) {
    console.error("Unable to parse structured AI result:", error);
    return null;
  }
}, [data]);

const dynamicKpis = structuredReport?.kpis || [];
const dynamicCharts = structuredReport?.charts || [];
const dynamicTable = structuredReport?.table;
const dynamicAnalysis = structuredReport?.analysis;

return (
    <main
      className="premium-background"
      style={{
        minHeight: "100vh",
        color: "#ffffff",
      }}
    >
      <div className="purple-glow purple-glow-one" />
      <div className="purple-glow purple-glow-two" />
      <div className="purple-glow purple-glow-three" />
      <div className="premium-grid" />

      <div
        style={{
          position: "relative",
          zIndex: 2,
          width: "100%",
          maxWidth: 1450,
          margin: "0 auto",
          padding: "30px 28px 60px",
        }}
      >
        {/* 1. HEADER SECTION */}
        <header style={{ marginBottom: 24 }}>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              flexWrap: "wrap",
              gap: 12,
              marginBottom: 12,
            }}
          >
            <Link
              href="/"
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: 6,
                color: "#a78bfa",
                fontSize: 13,
                fontWeight: 600,
                textDecoration: "none",
                padding: "7px 15px",
                borderRadius: 12,
                background: "rgba(139,92,246,0.12)",
                border: "1px solid rgba(139,92,246,0.22)",
                transition: "all 0.2s",
              }}
            >
             Back to Query
            </Link>

            <div style={{ display: "inline-flex", alignItems: "center", gap: 10 }}>
  <span
    style={{
      display: "inline-flex",
      alignItems: "center",
      gap: 6,
      padding: "5px 12px",
      borderRadius: 9999,
      background: "rgba(34, 211, 238, 0.12)",
      border: "1px solid rgba(34, 211, 238, 0.3)",
      fontSize: 12,
      fontWeight: 600,
      color: "#22d3ee",
    }}
  >
    {activeDomain}
  </span>

    <button
  type="button"
  onClick={downloadPDF}
  disabled={pdfLoading}
  style={{
    display: "inline-flex",
    alignItems: "center",
    gap: 6,
    padding: "6px 14px",
    borderRadius: 9999,
    border: "1px solid rgba(167, 139, 250, 0.35)",
    background:
      "linear-gradient(135deg, rgba(109, 40, 217, 0.35), rgba(192, 38, 211, 0.25))",
    color: "#ffffff",
    fontSize: 12,
    fontWeight: 600,
    cursor: pdfLoading ? "not-allowed" : "pointer",
    opacity: pdfLoading ? 0.6 : 1,
  }}
>
  {pdfLoading ? "Generating PDF..." : "Download PDF"}
</button>
              
              

              
            </div>
          </div>

          <div
            style={{
              fontSize: 11,
              fontWeight: 750,
              color: "#a78bfa",
              letterSpacing: "0.18em",
              textTransform: "uppercase",
              marginBottom: 4,
            }}
          >
            AI Business Intelligence
          </div>

          <h1
            style={{
              margin: 0,
              fontSize: "clamp(24px, 3vw, 36px)",
              lineHeight: 1.15,
              fontWeight: 750,
              letterSpacing: "-0.02em",
              color: "#ffffff",
            }}
          >
            Executive Analytics Dashboard
          </h1>

          <div
            style={{
              marginTop: 12,
              padding: "10px 16px",
              borderRadius: 12,
              background: "rgba(18,11,31,0.72)",
              border: "1px solid rgba(139,92,246,0.20)",
              color: "#c4b5fd",
              fontSize: 13,
              display: "flex",
              alignItems: "center",
              gap: 8,
              flexWrap: "wrap",
            }}
          >
            <strong style={{ color: "#ffffff" }}>Query:</strong>
            <span
              style={{
                color: "#22d3ee",
                fontWeight: 500,
                background: "rgba(34, 211, 238, 0.08)",
                padding: "2px 8px",
                borderRadius: 6,
              }}
            >
              &ldquo;{query}&rdquo;
            </span>
          </div>
        </header>
      
  {/* KPI CARDS */}
  {dynamicKpis.length > 0 && (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(210px, 1fr))",
        gap: 16,
        marginBottom: 20,
      }}
    >
      {dynamicKpis.map((kpi: any, index: number) => (
        <div
          key={`kpi-${index}`}
          style={{
            background: "rgba(18, 11, 31, 0.76)",
            border: "1px solid rgba(139,92,246,0.17)",
            borderRadius: 20,
            padding: "20px 22px",
            boxShadow: "0 20px 60px rgba(0,0,0,0.24)",
            backdropFilter: "blur(18px)",
          }}
        >
          <div
            style={{
              color: "#8f82a8",
              fontSize: 11,
              fontWeight: 700,
              textTransform: "uppercase",
              letterSpacing: "0.08em",
              marginBottom: 10,
            }}
          >
            {kpi.label}
          </div>

          <div
            style={{
              color: "#ffffff",
              fontSize: 26,
              fontWeight: 750,
              lineHeight: 1.2,
            }}
          >
            {kpi.value}
          </div>

          {kpi.unit && kpi.unit !== "text" && (
            <div
              style={{
                color: "#a78bfa",
                fontSize: 11,
                marginTop: 7,
              }}
            >
              {kpi.unit}
            </div>
          )}
        </div>
      ))}
    </div>
  )}

  {/* CHARTS */}
  {dynamicCharts.length > 0 && (
    <div
      style={{
        display: "grid",
        gridTemplateColumns:
          dynamicCharts.length === 1
            ? "minmax(0, 1fr)"
            : "repeat(2, minmax(0, 1fr))",
        gap: 18,
        marginBottom: 20,
      }}
    >
      {dynamicCharts.map((chart: any, index: number) => {

        const chartOption = {
          ...chartBase,

          tooltip: {
            trigger: chart.type === "pie" || chart.type === "donut"
              ? "item"
              : "axis",
            backgroundColor: "#170d29",
            borderColor: "#a855f7",
            textStyle: {
              color: "#ffffff",
            },
          },

          grid: {
            left: 55,
            right: 25,
            top: 45,
            bottom: 60,
            containLabel: true,
          },

          xAxis:
            chart.type === "pie" || chart.type === "donut"
              ? undefined
              : {
                  type: "category",
                  name: chart.x_axis || "",
                  data: (chart.data || []).map((item: any) => item.label),
                  axisLabel: {
                    color: "#a78bfa",
                    rotate:
                      (chart.data || []).length > 7 ? 35 : 0,
                  },
                  axisLine: {
                    lineStyle: {
                      color: "rgba(167,139,250,0.25)",
                    },
                  },
                },

          yAxis:
            chart.type === "pie" || chart.type === "donut"
              ? undefined
              : {
                  type: "value",
                  name: chart.y_axis || "",
                  axisLabel: {
                    color: "#a78bfa",
                  },
                  splitLine: {
                    lineStyle: {
                      color: "rgba(167,139,250,0.08)",
                    },
                  },
                },

          series: [
            {
              name: chart.title || "Value",

              type:
                chart.type === "donut"
                  ? "pie"
                  : chart.type,

              ...(chart.type === "pie" || chart.type === "donut"
                ? {
                    radius:
                      chart.type === "donut"
                        ? ["48%", "72%"]
                        : "65%",
                    center: ["50%", "48%"],
                    data: (chart.data || []).map((item: any) => ({
                      name: item.label,
                      value: Number(item.value) || 0,
                    })),
                    label: {
                      color: "#ffffff",
                    },
                  }
                : {
                    data: (chart.data || []).map(
                      (item: any) => Number(item.value) || 0
                    ),
                    smooth: chart.type === "line",
                    barMaxWidth: 55,
                  }),
            },
          ],
        };

        return (
          <ChartCard
            key={`chart-${index}`}
            title={chart.title || "Analytics"}
            subtitle={chart.description}
            chartType={
              chart.type
                ? chart.type.charAt(0).toUpperCase() +
                  chart.type.slice(1) +
                  " Chart"
                : undefined
            }
            option={chartOption}
            height={340}
          />
        );
      })}
    </div>
  )}

  {/* EXACT QUESTION-RELATED TABLE */}
  {dynamicTable && (
    <section
      style={{
        background: "rgba(18, 11, 31, 0.76)",
        border: "1px solid rgba(139,92,246,0.17)",
        borderRadius: 20,
        padding: "20px 22px",
        boxShadow: "0 20px 60px rgba(0,0,0,0.24)",
        backdropFilter: "blur(18px)",
        overflowX: "auto",
      }}
    >
      <div style={{ marginBottom: 16 }}>
        <h3
          style={{
            margin: 0,
            color: "#ffffff",
            fontSize: 16,
            fontWeight: 650,
          }}
        >
          {dynamicTable.title || "Related Data"}
        </h3>
      </div>

      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          fontSize: 13,
        }}
      >
        <thead>
          <tr>
            {(dynamicTable.columns || []).map(
              (column: string, index: number) => (
                <th
                  key={`head-${index}`}
                  style={{
                    textAlign: "left",
                    padding: "12px 10px",
                    color: "#c4b5fd",
                    borderBottom:
                      "1px solid rgba(139,92,246,0.18)",
                    fontWeight: 700,
                  }}
                >
                  {column}
                </th>
              )
            )}
          </tr>
        </thead>

        <tbody>
          {(dynamicTable.rows || []).map(
            (row: any, rowIndex: number) => (
              <tr key={`row-${rowIndex}`}>
                {(row.values || []).map(
                  (value: any, valueIndex: number) => (
                    <td
                      key={`cell-${rowIndex}-${valueIndex}`}
                      style={{
                        padding: "12px 10px",
                        color:
                          valueIndex === 0
                            ? "#ffffff"
                            : "#b8accb",
                        borderBottom:
                          "1px solid rgba(139,92,246,0.08)",
                      }}
                    >
                      {String(value)}
                    </td>
                  )
                )}
              </tr>
            )
          )}
        </tbody>
      </table>
    </section>
  )}

{/*10. FOOTER METADATA */}
        <footer
          style={{
            marginTop: 28,
            paddingTop: 16,
            borderTop: "1px solid rgba(139,92,246,0.12)",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            flexWrap: "wrap",
            gap: 10,
            fontSize: 12,
            color: "#8f82a8",
          }}
        >
          <div>
            Banking AI Reporting Platform â€¢ Real-time Business Intelligence Engine
          </div>
          <div style={{ color: "#a78bfa" }}>
            Generated via Gemini 3.5 Flash & PostgreSQL Live Analytics
          </div>
        </footer>
      </div>
    </main>
  );
}

