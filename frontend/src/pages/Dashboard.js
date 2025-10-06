import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useAuth } from '../contexts/AuthContext';
import { historyAPI } from '../services/api';
import { 
  BarChart3, 
  Camera, 
  TrendingUp, 
  Star, 
  Calendar,
  Trash2,
  Eye,
  Plus
} from 'lucide-react';

const Dashboard = () => {
  const { user } = useAuth();
  const [history, setHistory] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [historyData, statsData] = await Promise.all([
        historyAPI.getUserHistory({ limit: 20 }),
        historyAPI.getUserStats()
      ]);
      
      setHistory(historyData);
      setStats(statsData);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      toast.error('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteImage = async (imageId) => {
    if (!window.confirm('Are you sure you want to delete this analysis?')) {
      return;
    }

    setDeleting(imageId);
    
    try {
      await historyAPI.deleteImage(imageId);
      setHistory(history.filter(item => item.id !== imageId));
      toast.success('Analysis deleted successfully');
      
      // Refresh stats
      const statsData = await historyAPI.getUserStats();
      setStats(statsData);
    } catch (error) {
      console.error('Error deleting image:', error);
      toast.error('Failed to delete analysis');
    } finally {
      setDeleting(null);
    }
  };

  const getRatingColor = (rating) => {
    if (rating >= 8) return 'text-green-600 bg-green-100';
    if (rating >= 6) return 'text-yellow-600 bg-yellow-100';
    if (rating >= 4) return 'text-orange-600 bg-orange-100';
    return 'text-red-600 bg-red-100';
  };

  const getRatingLabel = (rating) => {
    if (rating >= 9) return 'Exceptional';
    if (rating >= 8) return 'Excellent';
    if (rating >= 7) return 'Very Good';
    if (rating >= 6) return 'Good';
    if (rating >= 5) return 'Average';
    if (rating >= 4) return 'Below Average';
    return 'Poor';
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="loading-spinner mx-auto mb-4"></div>
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Welcome back, {user?.username}!
          </h1>
          <p className="text-gray-600">
            Manage your camel analysis history and track your progress
          </p>
        </div>

        {/* Stats Cards */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div className="card p-6">
              <div className="flex items-center">
                <div className="w-12 h-12 bg-camel-100 rounded-lg flex items-center justify-center">
                  <Camera className="w-6 h-6 text-camel-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Total Analyses</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.total_images}</p>
                </div>
              </div>
            </div>

            <div className="card p-6">
              <div className="flex items-center">
                <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                  <Star className="w-6 h-6 text-green-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Average Rating</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.average_rating}</p>
                </div>
              </div>
            </div>

            <div className="card p-6">
              <div className="flex items-center">
                <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
                  <TrendingUp className="w-6 h-6 text-yellow-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Highest Rating</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.highest_rating}</p>
                </div>
              </div>
            </div>

            <div className="card p-6">
              <div className="flex items-center">
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                  <BarChart3 className="w-6 h-6 text-blue-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Lowest Rating</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.lowest_rating}</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Quick Actions */}
        <div className="mb-8">
          <div className="flex flex-col sm:flex-row gap-4">
            <Link to="/" className="btn-primary flex items-center space-x-2">
              <Plus className="w-4 h-4" />
              <span>New Analysis</span>
            </Link>
            
            {stats && stats.total_images > 0 && (
              <div className="flex items-center space-x-4 text-sm text-gray-600">
                <div className="flex items-center space-x-1">
                  <Calendar className="w-4 h-4" />
                  <span>Last analysis: {new Date(history[0]?.created_at).toLocaleDateString()}</span>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* History Section */}
        <div className="card p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold text-gray-900">Recent Analyses</h2>
            {history.length > 0 && (
              <Link 
                to="/history" 
                className="text-camel-600 hover:text-camel-500 text-sm font-medium"
              >
                View All
              </Link>
            )}
          </div>

          {history.length === 0 ? (
            <div className="text-center py-12">
              <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Camera className="w-8 h-8 text-gray-400" />
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                No analyses yet
              </h3>
              <p className="text-gray-600 mb-6">
                Start by uploading your first camel image for analysis
              </p>
              <Link to="/" className="btn-primary">
                <Camera className="w-4 h-4 mr-2" />
                Upload First Image
              </Link>
            </div>
          ) : (
            <div className="space-y-4">
              {history.map((item) => (
                <div key={item.id} className="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg">
                  <img
                    src={`http://localhost:8000${item.image_url}`}
                    alt="Camel analysis"
                    className="w-16 h-16 object-cover rounded-lg"
                  />
                  
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center space-x-2 mb-1">
                      <span className={`px-2 py-1 rounded-full text-sm font-medium ${getRatingColor(item.rating)}`}>
                        {item.rating}/10
                      </span>
                      <span className="text-sm text-gray-600">
                        {getRatingLabel(item.rating)}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600">
                      {new Date(item.created_at).toLocaleDateString()} at {new Date(item.created_at).toLocaleTimeString()}
                    </p>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    <Link
                      to={`/results/${item.id}`}
                      className="p-2 text-gray-400 hover:text-camel-600 transition-colors duration-200"
                      title="View details"
                    >
                      <Eye className="w-4 h-4" />
                    </Link>
                    
                    <button
                      onClick={() => handleDeleteImage(item.id)}
                      disabled={deleting === item.id}
                      className="p-2 text-gray-400 hover:text-red-600 transition-colors duration-200 disabled:opacity-50"
                      title="Delete analysis"
                    >
                      {deleting === item.id ? (
                        <div className="loading-spinner w-4 h-4"></div>
                      ) : (
                        <Trash2 className="w-4 h-4" />
                      )}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Rating Distribution */}
        {stats && stats.rating_distribution && Object.keys(stats.rating_distribution).length > 0 && (
          <div className="mt-8 card p-6">
            <h3 className="text-lg font-bold text-gray-900 mb-4">
              Rating Distribution
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
              {Object.entries(stats.rating_distribution)
                .sort(([a], [b]) => parseInt(a) - parseInt(b))
                .map(([rating, count]) => (
                  <div key={rating} className="text-center">
                    <div className="text-2xl font-bold text-camel-600 mb-1">
                      {count}
                    </div>
                    <div className="text-sm text-gray-600">
                      {rating}/10 ratings
                    </div>
                  </div>
                ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
