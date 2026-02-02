import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  RefreshControl,
  TouchableOpacity,
  ActivityIndicator,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useAuth } from '../../contexts/AuthContext';
import { Ionicons } from '@expo/vector-icons';
import axios from 'axios';

const EXPO_PUBLIC_BACKEND_URL = process.env.EXPO_PUBLIC_BACKEND_URL;
const API_URL = `${EXPO_PUBLIC_BACKEND_URL}/api`;

interface Stats {
  total_orders: number;
  pending_orders: number;
  completed_orders: number;
  total_products: number;
  low_stock_products: number;
  total_vendors: number;
  pending_payments: number;
  total_revenue: number;
}

export default function DashboardScreen() {
  const { user, token } = useAuth();
  const [stats, setStats] = useState<Stats | null>(null);
  const [refreshing, setRefreshing] = useState(false);
  const [loading, setLoading] = useState(true);

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API_URL}/dashboard/stats`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    if (token) {
      fetchStats();
    }
  }, [token]);

  const onRefresh = () => {
    setRefreshing(true);
    fetchStats();
  };

  const getRoleColor = (role: string) => {
    switch (role) {
      case 'Admin':
        return '#FF3B30';
      case 'Sales':
        return '#34C759';
      case 'Buyer':
        return '#007AFF';
      default:
        return '#8E8E93';
    }
  };

  const StatCard = ({ title, value, icon, color }: any) => (
    <View style={[styles.statCard, { borderLeftColor: color }]}>
      <View style={styles.statHeader}>
        <Ionicons name={icon} size={24} color={color} />
        <Text style={styles.statValue}>{value}</Text>
      </View>
      <Text style={styles.statTitle}>{title}</Text>
    </View>
  );

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#007AFF" />
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.container} edges={['bottom']}>
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >
        {/* User Info Card */}
        <View style={styles.userCard}>
          <View style={styles.userInfo}>
            <View style={styles.avatar}>
              <Text style={styles.avatarText}>
                {user?.name?.charAt(0).toUpperCase()}
              </Text>
            </View>
            <View style={styles.userDetails}>
              <Text style={styles.userName}>{user?.name}</Text>
              <Text style={styles.userEmail}>{user?.email}</Text>
            </View>
          </View>
          <View style={[styles.roleBadge, { backgroundColor: getRoleColor(user?.role || '') + '20' }]}>
            <Text style={[styles.roleText, { color: getRoleColor(user?.role || '') }]}>
              {user?.role}
            </Text>
          </View>
        </View>

        {/* Company Info */}
        {user?.company_name && (
          <View style={styles.companyCard}>
            <Ionicons name="business-outline" size={20} color="#007AFF" />
            <Text style={styles.companyName}>{user.company_name}</Text>
          </View>
        )}

        {/* Stats Grid */}
        <View style={styles.statsSection}>
          <Text style={styles.sectionTitle}>Overview</Text>
          
          <View style={styles.statsGrid}>
            {/* Show stats based on role */}
            {(user?.role === 'Admin' || user?.role === 'Sales') && (
              <>
                <StatCard
                  title="Total Orders"
                  value={stats?.total_orders || 0}
                  icon="cart-outline"
                  color="#007AFF"
                />
                <StatCard
                  title="Pending Orders"
                  value={stats?.pending_orders || 0}
                  icon="time-outline"
                  color="#FF9500"
                />
                <StatCard
                  title="Completed Orders"
                  value={stats?.completed_orders || 0}
                  icon="checkmark-circle-outline"
                  color="#34C759"
                />
                <StatCard
                  title="Total Products"
                  value={stats?.total_products || 0}
                  icon="cube-outline"
                  color="#5856D6"
                />
              </>
            )}

            {user?.role === 'Admin' && (
              <>
                <StatCard
                  title="Low Stock Items"
                  value={stats?.low_stock_products || 0}
                  icon="alert-circle-outline"
                  color="#FF3B30"
                />
                <StatCard
                  title="Total Vendors"
                  value={stats?.total_vendors || 0}
                  icon="people-outline"
                  color="#AF52DE"
                />
              </>
            )}

            {(user?.role === 'Admin' || user?.role === 'Sales' || user?.role === 'Buyer') && (
              <>
                <StatCard
                  title="Pending Payments"
                  value={stats?.pending_payments || 0}
                  icon="wallet-outline"
                  color="#FF9500"
                />
                <StatCard
                  title="Total Revenue"
                  value={`$${stats?.total_revenue?.toFixed(2) || '0.00'}`}
                  icon="trending-up-outline"
                  color="#34C759"
                />
              </>
            )}

            {user?.role === 'Buyer' && (
              <>
                <StatCard
                  title="My Orders"
                  value={stats?.total_orders || 0}
                  icon="cart-outline"
                  color="#007AFF"
                />
                <StatCard
                  title="Pending Orders"
                  value={stats?.pending_orders || 0}
                  icon="time-outline"
                  color="#FF9500"
                />
              </>
            )}
          </View>
        </View>

        {/* Quick Actions */}
        <View style={styles.actionsSection}>
          <Text style={styles.sectionTitle}>Quick Actions</Text>
          
          <View style={styles.actionsGrid}>
            {(user?.role === 'Admin' || user?.role === 'Sales') && (
              <TouchableOpacity style={styles.actionButton}>
                <Ionicons name="add-circle-outline" size={32} color="#007AFF" />
                <Text style={styles.actionText}>Create Order</Text>
              </TouchableOpacity>
            )}

            {user?.role === 'Admin' && (
              <TouchableOpacity style={styles.actionButton}>
                <Ionicons name="person-add-outline" size={32} color="#34C759" />
                <Text style={styles.actionText}>Add User</Text>
              </TouchableOpacity>
            )}

            {(user?.role === 'Admin' || user?.role === 'Sales') && (
              <TouchableOpacity style={styles.actionButton}>
                <Ionicons name="cube-outline" size={32} color="#5856D6" />
                <Text style={styles.actionText}>Add Product</Text>
              </TouchableOpacity>
            )}

            {user?.role === 'Buyer' && (
              <TouchableOpacity style={styles.actionButton}>
                <Ionicons name="card-outline" size={32} color="#FF9500" />
                <Text style={styles.actionText}>Make Payment</Text>
              </TouchableOpacity>
            )}
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  scrollContent: {
    padding: 16,
  },
  userCard: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 16,
    marginBottom: 16,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  userInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  avatar: {
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: '#007AFF',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  avatarText: {
    color: '#fff',
    fontSize: 24,
    fontWeight: 'bold',
  },
  userDetails: {
    flex: 1,
  },
  userName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1a1a1a',
    marginBottom: 4,
  },
  userEmail: {
    fontSize: 14,
    color: '#666',
  },
  roleBadge: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 8,
  },
  roleText: {
    fontSize: 14,
    fontWeight: '600',
  },
  companyCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    flexDirection: 'row',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  companyName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1a1a1a',
    marginLeft: 8,
  },
  statsSection: {
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#1a1a1a',
    marginBottom: 16,
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  statCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    width: '48%',
    borderLeftWidth: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  statHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  statValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#1a1a1a',
  },
  statTitle: {
    fontSize: 13,
    color: '#666',
  },
  actionsSection: {
    marginBottom: 16,
  },
  actionsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  actionButton: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 20,
    alignItems: 'center',
    justifyContent: 'center',
    width: '48%',
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  actionText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#1a1a1a',
    marginTop: 8,
    textAlign: 'center',
  },
});
