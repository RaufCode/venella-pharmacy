// utils/notification.js
import axios from 'axios'

/**
 * Send a notification to all salespersons.
 * 
 * @param {string} content - Notification message.
 * @param {'NEW_ORDER'|'LOW_STOCK'|'ORDER_PROCESSED'|'DELIVERED'|'CANCELLED'} type - Notification type.
 */
export async function notifySalesperson(content, type = 'NEW_ORDER') {
  try {
    await axios.post('/api/notifications/sales-person/', {
      content,
      type
    })
    console.log(`[Notification Sent] ${type}: ${content}`)
  } catch (error) {
    console.error('❌ Failed to send salesperson notification:', error)
  }
}

/**
 * Mark a specific notification as read.
 * 
 * @param {string} notificationId - The UUID of the notification.
 */
export async function markNotificationAsRead(notificationId) {
  try {
    await axios.post(`/api/notifications/${notificationId}/mark-as-read/`)
    console.log(`✅ Notification ${notificationId} marked as read`)
  } catch (error) {
    console.error(`❌ Failed to mark notification ${notificationId} as read:`, error)
  }
}
