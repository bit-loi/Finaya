import { useState } from 'react';

const escapeXml = (value) => String(value ?? '')
  .replaceAll('&', '&amp;')
  .replaceAll('<', '&lt;')
  .replaceAll('>', '&gt;')
  .replaceAll('"', '&quot;')
  .replaceAll("'", '&apos;');

const worksheetName = (name) => escapeXml(name).slice(0, 31);

const buildWorksheet = ({ name, rows }) => `
  <Worksheet ss:Name="${worksheetName(name)}">
    <Table>
      ${rows.map((row) => `
        <Row>
          ${row.map((cell) => `<Cell><Data ss:Type="${typeof cell === 'number' ? 'Number' : 'String'}">${escapeXml(cell)}</Data></Cell>`).join('')}
        </Row>
      `).join('')}
    </Table>
  </Worksheet>`;

const downloadWorkbook = (sheets, filename) => {
  const workbook = `<?xml version="1.0"?>
<?mso-application progid="Excel.Sheet"?>
<Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet"
  xmlns:o="urn:schemas-microsoft-com:office:office"
  xmlns:x="urn:schemas-microsoft-com:office:excel"
  xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet"
  xmlns:html="http://www.w3.org/TR/REC-html40">
  ${sheets.map(buildWorksheet).join('')}
</Workbook>`;

  const blob = new Blob([workbook], { type: 'application/vnd.ms-excel;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');

  link.href = url;
  link.download = `${filename}.xls`;
  link.style.display = 'none';

  document.body.appendChild(link);
  link.click();

  setTimeout(() => {
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  }, 100);
};

export const useExcelExport = () => {
  const [isExporting, setIsExporting] = useState(false);

  const formatCurrency = (value) => {
    if (!value && value !== 0) return 'Rp 0';
    return `Rp ${Number(value).toLocaleString('id-ID')}`;
  };

  const formatNumber = (value) => {
    if (!value && value !== 0) return '0';
    return Number(value).toLocaleString('id-ID');
  };

  const exportToExcel = async (analysisData, filename = 'analysis_report') => {
    setIsExporting(true);

    try {
      const metrics = analysisData.metrics || {};
      const areaDistribution = analysisData.areaDistribution;
      const swot = areaDistribution?.swot;

      const sheets = [
        {
          name: 'Executive Summary',
          rows: [
            ['FINAYA BUSINESS ANALYSIS REPORT'],
            [],
            ['Analysis Information'],
            ['Location Name', analysisData.locationName || analysisData.name || 'N/A'],
            ['Address', analysisData.locationData?.address || analysisData.location || 'N/A'],
            ['Analysis Date', new Date().toLocaleDateString('id-ID', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })],
            ['Report Generated', new Date().toLocaleString('id-ID')],
            [],
            ['KEY PERFORMANCE METRICS'],
            [],
            ['Revenue Analysis'],
            ['Total Purchases per Day', `${formatNumber(metrics.tppd || 0)} transactions`],
            ['Daily Revenue', formatCurrency(metrics.dailyRevenue || 0)],
            ['Monthly Revenue', formatCurrency(metrics.monthlyRevenue || 0)],
            ['Yearly Revenue (Projected)', formatCurrency(metrics.yearlyRevenue || 0)],
            [],
            ['Location Assessment'],
            ['Location Score', `${metrics.locationScore || 0} / 10`],
            ['Risk Score', `${((metrics.riskScore || 0) * 100).toFixed(1)}%`],
            ['Confidence Level', metrics.confidenceLevel || 'N/A'],
          ],
        },
        {
          name: 'Technical Analysis',
          rows: [
            ['TECHNICAL BREAKDOWN'],
            [],
            ['Population & Demographics'],
            ['CGLP Population', `${formatNumber(metrics.cglp || 0)} people`],
            ['Residential Population', `${formatNumber(metrics.pops || 0)} people`],
            [],
            ['Traffic & Infrastructure'],
            ['Traffic Potential (APT)', `${formatNumber(metrics.apt || 0)} vehicles/day`],
            ['Road Density (PDR)', `${metrics.pdr || 0} km/km2`],
            [],
            ['Area Analysis'],
            ['Analysis Zone Area', `${(analysisData.locationData?.areaSquareKm || 0).toFixed(4)} km2`],
            ['Catchment Radius', '500 meters (default)'],
          ],
        },
        {
          name: 'Financial Projections',
          rows: [
            ['FINANCIAL PROJECTIONS'],
            [],
            ['Revenue Breakdown'],
            ['Period', 'Amount (IDR)'],
            ['Daily Revenue', formatCurrency(metrics.dailyRevenue || 0)],
            ['Weekly Revenue (7 days)', formatCurrency((metrics.dailyRevenue || 0) * 7)],
            ['Monthly Revenue (30 days)', formatCurrency(metrics.monthlyRevenue || 0)],
            ['Quarterly Revenue (90 days)', formatCurrency((metrics.monthlyRevenue || 0) * 3)],
            ['Yearly Revenue (365 days)', formatCurrency(metrics.yearlyRevenue || 0)],
            [],
            ['Transaction Metrics'],
            ['Purchases per Day', `${formatNumber(metrics.tppd || 0)} transactions`],
            ['Purchases per Month', `${formatNumber((metrics.tppd || 0) * 30)} transactions`],
            ['Purchases per Year', `${formatNumber((metrics.tppd || 0) * 365)} transactions`],
            [],
            ['Average Transaction'],
            ['Avg Transaction Value', formatCurrency((metrics.dailyRevenue || 0) / (metrics.tppd || 1))],
          ],
        },
        {
          name: 'Risk Analysis',
          rows: [
            ['RISK EVALUATION'],
            [],
            ['Risk Assessment'],
            ['Risk Score', `${((metrics.riskScore || 0) * 100).toFixed(1)}%`],
            ['Risk Category', (metrics.riskScore || 0) > 0.5 ? 'High Risk' : (metrics.riskScore || 0) > 0.3 ? 'Medium Risk' : 'Low Risk'],
            ['Confidence Level', metrics.confidenceLevel || 'N/A'],
            [],
            ['Model Information'],
            ['Assumptions', metrics.assumptions || 'Standard urban density model applied.'],
            [],
            ['Risk Interpretation'],
            ['Score Range', 'Meaning'],
            ['0% - 30%', 'Low Risk - High stability and profitability potential'],
            ['31% - 50%', 'Medium Risk - Moderate stability, careful planning needed'],
            ['51% - 100%', 'High Risk - Significant challenges, thorough analysis required'],
          ],
        },
        {
          name: 'Raw Data',
          rows: [
            ['RAW DATA EXPORT'],
            [],
            ['All Metrics (Unformatted)'],
            ['Metric', 'Value'],
            ['TPPD', metrics.tppd || 0],
            ['Daily Revenue', metrics.dailyRevenue || 0],
            ['Monthly Revenue', metrics.monthlyRevenue || 0],
            ['Yearly Revenue', metrics.yearlyRevenue || 0],
            ['Location Score', metrics.locationScore || 0],
            ['Risk Score (decimal)', metrics.riskScore || 0],
            ['CGLP', metrics.cglp || 0],
            ['POPS', metrics.pops || 0],
            ['APT', metrics.apt || 0],
            ['PDR', metrics.pdr || 0],
            ['Area (km2)', analysisData.locationData?.areaSquareKm || 0],
            [],
            ['Use this sheet for further calculations and analysis'],
          ],
        },
      ];

      if (areaDistribution) {
        sheets.splice(4, 0, {
          name: 'Area Distribution',
          rows: [
            ['AREA DISTRIBUTION ANALYSIS'],
            [],
            ['Land Use Breakdown'],
            ['Category', 'Percentage', 'Description'],
            ['Residential Area', `${areaDistribution.residential || 0}%`, 'Housing and living spaces'],
            ['Road Network', `${areaDistribution.road || 0}%`, 'Streets and transportation infrastructure'],
            ['Open Space', `${areaDistribution.openSpace || 0}%`, 'Parks, green areas, and public spaces'],
            [],
            ['AI Analysis - Area Reasoning'],
            [areaDistribution.reasoning || 'N/A'],
            [],
            ['Impact on Business'],
            ['High Residential % = More potential customers living nearby'],
            ['High Road % = Better accessibility and traffic flow'],
            ['Balanced distribution generally indicates stable commercial area'],
          ],
        });
      }

      if (swot) {
        sheets.splice(5, 0, {
          name: 'AI Strategic Insights',
          rows: [
            ['AI STRATEGIC INSIGHTS - SWOT ANALYSIS'],
            [],
            ['STRENGTHS - Internal Positive Factors'],
            ...(swot.strengths?.length ? swot.strengths.map((item, index) => [`${index + 1}.`, item]) : [['', 'No strengths identified']]),
            [],
            ['WEAKNESSES - Internal Negative Factors'],
            ...(swot.weaknesses?.length ? swot.weaknesses.map((item, index) => [`${index + 1}.`, item]) : [['', 'No weaknesses identified']]),
            [],
            ['OPPORTUNITIES - External Positive Factors'],
            ...(swot.opportunities?.length ? swot.opportunities.map((item, index) => [`${index + 1}.`, item]) : [['', 'No opportunities identified']]),
            [],
            ['THREATS - External Negative Factors'],
            ...(swot.threats?.length ? swot.threats.map((item, index) => [`${index + 1}.`, item]) : [['', 'No threats identified']]),
            [],
            ['STRATEGIC RECOMMENDATIONS'],
            ['Leverage strengths to capitalize on opportunities'],
            ['Address weaknesses to mitigate threats'],
            ['Develop contingency plans for identified risks'],
            ['Monitor market trends and adjust strategy accordingly'],
          ],
        });
      }

      downloadWorkbook(sheets, filename);
      return { success: true };
    } catch (error) {
      console.error('Excel export failed:', error);
      return { success: false, error };
    } finally {
      setTimeout(() => setIsExporting(false), 200);
    }
  };

  return { exportToExcel, isExporting };
};
