import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useAuth } from '../../contexts/AuthContext';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

export default function ProfileScreen() {
  const { user, logout } = useAuth();
  const router = useRouter();

  const handleLogout = () => {
    Alert.alert(
      'Logout',
      'Are you sure you want to logout?',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Logout',
          style: 'destructive',
          onPress: async () => {
            await logout();
            router.replace('/auth/login');
          },
        },
      ]
    );
  };

  const ProfileItem = ({ icon, label, value }: any) => (
    <View style={styles.profileItem}>
      <View style={styles.itemLeft}>
        <Ionicons name={icon} size={24} color="#007AFF" />
        <Text style={styles.itemLabel}>{label}</Text>
      </View>
      <Text style={styles.itemValue}>{value}</Text>
    </View>
  );

  return (
    <SafeAreaView style={styles.container} edges={['bottom']}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        {/* Profile Header */}
        <View style={styles.header}>
          <View style={styles.avatarLarge}>
            <Text style={styles.avatarTextLarge}>
              {user?.name?.charAt(0).toUpperCase()}
            </Text>
          </View>
          <Text style={styles.name}>{user?.name}</Text>
          <View style={styles.roleBadge}>
            <Text style={styles.roleText}>{user?.role}</Text>
          </View>
        </View>

        {/* Profile Details */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Account Information</Text>
          <View style={styles.card}>
            <ProfileItem icon="mail-outline" label="Email" value={user?.email} />
            <ProfileItem icon="call-outline" label="Mobile" value={user?.mobile} />
            <ProfileItem icon="business-outline" label="Company" value={user?.company_name || 'N/A'} />
            <ProfileItem icon="shield-outline" label="Role" value={user?.role} />
          </View>
        </View>

        {/* Actions */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Settings</Text>
          <TouchableOpacity style={styles.actionCard}>
            <Ionicons name="notifications-outline" size={24} color="#007AFF" />
            <Text style={styles.actionText}>Notifications</Text>
            <Ionicons name="chevron-forward-outline" size={24} color="#8E8E93" />
          </TouchableOpacity>
          <TouchableOpacity style={styles.actionCard}>
            <Ionicons name="lock-closed-outline" size={24} color="#007AFF" />
            <Text style={styles.actionText}>Change Password</Text>
            <Ionicons name="chevron-forward-outline" size={24} color="#8E8E93" />
          </TouchableOpacity>
          <TouchableOpacity style={styles.actionCard}>
            <Ionicons name="help-circle-outline" size={24} color="#007AFF" />
            <Text style={styles.actionText}>Help & Support</Text>
            <Ionicons name="chevron-forward-outline" size={24} color="#8E8E93" />
          </TouchableOpacity>
        </View>

        {/* Logout Button */}
        <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
          <Ionicons name="log-out-outline" size={24} color="#fff" />
          <Text style={styles.logoutText}>Logout</Text>
        </TouchableOpacity>

        <Text style={styles.version}>Version 1.0.0</Text>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  scrollContent: {
    padding: 16,
  },
  header: {
    alignItems: 'center',
    marginBottom: 32,
    marginTop: 16,
  },
  avatarLarge: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: '#007AFF',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
  },
  avatarTextLarge: {
    color: '#fff',
    fontSize: 40,
    fontWeight: 'bold',
  },
  name: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#1a1a1a',
    marginBottom: 8,
  },
  roleBadge: {
    backgroundColor: '#007AFF',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
  },
  roleText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
  },
  section: {
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#1a1a1a',
    marginBottom: 12,
    marginLeft: 4,
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  profileItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 16,
    paddingHorizontal: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  itemLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  itemLabel: {
    fontSize: 16,
    color: '#666',
    marginLeft: 12,
  },
  itemValue: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1a1a1a',
    flex: 1,
    textAlign: 'right',
  },
  actionCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  actionText: {
    fontSize: 16,
    color: '#1a1a1a',
    marginLeft: 12,
    flex: 1,
  },
  logoutButton: {
    backgroundColor: '#FF3B30',
    borderRadius: 12,
    padding: 16,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 16,
  },
  logoutText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
    marginLeft: 8,
  },
  version: {
    textAlign: 'center',
    color: '#8E8E93',
    fontSize: 12,
    marginTop: 24,
    marginBottom: 16,
  },
});
