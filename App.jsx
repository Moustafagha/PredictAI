import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { AlertCircle, Activity, Thermometer, Zap, Gauge } from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import './App.css'

// API base URL - will work with both local development and deployment
const API_BASE_URL = process.env.NODE_ENV === 'development' ? 'http://localhost:5000/api' : '/api'

function App() {
  const [machineData, setMachineData] = useState(null)
  const [historicalData, setHistoricalData] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Fetch current machine status
  const fetchMachineStatus = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/machine-status`)
      const result = await response.json()
      
      if (result.success) {
        setMachineData(result.data)
        setError(null)
      } else {
        setError(result.error || 'Failed to fetch machine status')
      }
    } catch (err) {
      setError('Network error: Unable to connect to server')
      console.error('Error fetching machine status:', err)
    }
  }

  // Fetch historical data
  const fetchHistoricalData = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/historical-data?limit=20`)
      const result = await response.json()
      
      if (result.success) {
        // Format data for chart
        const formattedData = result.data.map((item, index) => ({
          time: index + 1,
          temperature: item.temperature,
          vibration: item.vibration * 100, // Scale for better visualization
          pressure: item.pressure,
          failureProbability: item.failure_probability
        }))
        setHistoricalData(formattedData)
      }
    } catch (err) {
      console.error('Error fetching historical data:', err)
    }
  }

  // Auto-refresh data
  useEffect(() => {
    const fetchData = async () => {
      setLoading(true)
      await Promise.all([fetchMachineStatus(), fetchHistoricalData()])
      setLoading(false)
    }

    fetchData()
    
    // Refresh every 5 seconds
    const interval = setInterval(fetchData, 5000)
    
    return () => clearInterval(interval)
  }, [])

  // Get status color and icon
  const getStatusInfo = (status, alertLevel) => {
    switch (alertLevel) {
      case 'normal':
        return { color: 'bg-green-500', textColor: 'text-green-700', icon: Activity }
      case 'warning':
        return { color: 'bg-yellow-500', textColor: 'text-yellow-700', icon: AlertCircle }
      case 'critical':
        return { color: 'bg-red-500', textColor: 'text-red-700', icon: AlertCircle }
      default:
        return { color: 'bg-gray-500', textColor: 'text-gray-700', icon: Activity }
    }
  }

  if (loading && !machineData) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  if (error && !machineData) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
          <p className="text-red-600 mb-4">{error}</p>
          <button 
            onClick={() => window.location.reload()} 
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  const statusInfo = machineData ? getStatusInfo(machineData.current_status, machineData.alert_level) : null
  const StatusIcon = statusInfo?.icon || Activity

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Predictive Failure Monitor
          </h1>
          <p className="text-gray-600">Real-time machine health monitoring with AI predictions</p>
        </div>

        {/* Machine Status Section */}
        <div className="mb-8">
          <Card className="border-l-4 border-l-blue-500">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="text-lg">{machineData?.machine_name || 'Machine Monitor'}</CardTitle>
                  <p className="text-sm text-gray-600">ID: {machineData?.machine_id || 'N/A'}</p>
                </div>
                <div className="flex items-center space-x-2">
                  <div className={`w-3 h-3 rounded-full ${statusInfo?.color}`}></div>
                  <StatusIcon className={`h-5 w-5 ${statusInfo?.textColor}`} />
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="flex items-center space-x-4">
                <div>
                  <p className="text-2xl font-bold text-gray-900">
                    {machineData?.current_status || 'Unknown'}
                  </p>
                  <p className="text-sm text-gray-600">Current Status</p>
                </div>
                <Badge variant={machineData?.alert_level === 'critical' ? 'destructive' : 
                              machineData?.alert_level === 'warning' ? 'secondary' : 'default'}>
                  {machineData?.alert_level || 'unknown'}
                </Badge>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Dashboard Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          {/* Sensor Readings */}
          <div className="lg:col-span-2 space-y-4">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Real-time Sensor Readings</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Temperature */}
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Temperature</CardTitle>
                  <Thermometer className="h-4 w-4 text-red-500" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">
                    {machineData?.sensor_readings?.temperature || 0}°C
                  </div>
                  <p className="text-xs text-muted-foreground">Operating temperature</p>
                </CardContent>
              </Card>

              {/* Vibration */}
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Vibration</CardTitle>
                  <Zap className="h-4 w-4 text-yellow-500" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">
                    {machineData?.sensor_readings?.vibration || 0} m/s²
                  </div>
                  <p className="text-xs text-muted-foreground">Vibration level</p>
                </CardContent>
              </Card>

              {/* Pressure */}
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Pressure</CardTitle>
                  <Gauge className="h-4 w-4 text-blue-500" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">
                    {machineData?.sensor_readings?.pressure || 0} psi
                  </div>
                  <p className="text-xs text-muted-foreground">System pressure</p>
                </CardContent>
              </Card>
            </div>
          </div>

          {/* Failure Probability */}
          <div>
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Failure Prediction</h2>
            <Card className="h-fit">
              <CardHeader className="text-center">
                <CardTitle className="text-sm font-medium">FAILURE PROBABILITY</CardTitle>
              </CardHeader>
              <CardContent className="text-center">
                <div className={`text-6xl font-bold mb-2 ${statusInfo?.textColor}`}>
                  {Math.round(machineData?.failure_probability || 0)}%
                </div>
                <p className="text-sm text-muted-foreground mb-4">
                  AI-powered prediction based on current sensor data
                </p>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className={`h-2 rounded-full transition-all duration-500 ${statusInfo?.color}`}
                    style={{ width: `${Math.min(machineData?.failure_probability || 0, 100)}%` }}
                  ></div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Historical Trends Chart */}
        <Card>
          <CardHeader>
            <CardTitle>Historical Data Trends</CardTitle>
            <p className="text-sm text-muted-foreground">
              Recent sensor readings and failure probability over time
            </p>
          </CardHeader>
          <CardContent>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={historicalData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="time" />
                  <YAxis />
                  <Tooltip 
                    formatter={(value, name) => {
                      if (name === 'vibration') return [(value / 100).toFixed(2), 'Vibration (m/s²)']
                      if (name === 'failureProbability') return [value.toFixed(1) + '%', 'Failure Probability']
                      return [value, name]
                    }}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="temperature" 
                    stroke="#ef4444" 
                    strokeWidth={2}
                    name="Temperature (°C)"
                  />
                  <Line 
                    type="monotone" 
                    dataKey="vibration" 
                    stroke="#f59e0b" 
                    strokeWidth={2}
                    name="vibration"
                  />
                  <Line 
                    type="monotone" 
                    dataKey="pressure" 
                    stroke="#3b82f6" 
                    strokeWidth={2}
                    name="Pressure (psi)"
                  />
                  <Line 
                    type="monotone" 
                    dataKey="failureProbability" 
                    stroke="#8b5cf6" 
                    strokeWidth={3}
                    name="failureProbability"
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        {/* Footer */}
        <div className="mt-8 text-center text-sm text-gray-500">
          <p>Last updated: {machineData?.last_updated ? new Date(machineData.last_updated * 1000).toLocaleTimeString() : 'N/A'}</p>
          <p>Auto-refresh every 5 seconds</p>
        </div>
      </div>
    </div>
  )
}

export default App

