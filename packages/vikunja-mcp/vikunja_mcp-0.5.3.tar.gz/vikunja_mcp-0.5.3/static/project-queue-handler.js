/**
 * Project Queue Handler
 * 
 * Polls the project creation queue and creates projects using the user's session token.
 * This runs on page load in Vikunja to handle queued project creation requests.
 * 
 * Bead: solutions-eofy (User Can Create Project)
 */

(function() {
  'use strict';

  const CONFIG = {
    mcp_url: 'https://mcp.factumerit.app',
    vikunja_api: '/api/v1',
    poll_on_load: true,
    show_notifications: true
  };

  /**
   * Get user's JWT token from localStorage
   */
  function getToken() {
    return localStorage.getItem('token');
  }

  /**
   * Fetch pending projects from queue
   */
  async function fetchQueue() {
    const token = getToken();
    if (!token) {
      console.log('[project-queue] No token found, skipping queue check');
      return [];
    }

    try {
      const response = await fetch(`${CONFIG.mcp_url}/project-queue`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        console.error('[project-queue] Failed to fetch queue:', response.status);
        return [];
      }

      const data = await response.json();
      return data.queue || [];
    } catch (error) {
      console.error('[project-queue] Error fetching queue:', error);
      return [];
    }
  }

  /**
   * Create a project in Vikunja
   */
  async function createProject(item) {
    const token = getToken();
    const payload = {
      title: item.title
    };

    if (item.description) payload.description = item.description;
    if (item.hex_color) payload.hex_color = item.hex_color;
    if (item.parent_project_id) payload.parent_project_id = item.parent_project_id;

    const response = await fetch(`${CONFIG.vikunja_api}/projects`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error(`Failed to create project: ${response.status}`);
    }

    return await response.json();
  }

  /**
   * Share project with bot
   */
  async function shareWithBot(projectId, botUsername) {
    const token = getToken();
    
    // First, get bot's user ID by searching for the username
    const searchResponse = await fetch(`${CONFIG.vikunja_api}/users?s=${encodeURIComponent(botUsername)}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!searchResponse.ok) {
      throw new Error(`Failed to find bot user: ${searchResponse.status}`);
    }

    const users = await searchResponse.json();
    const botUser = users.find(u => u.username === botUsername);
    
    if (!botUser) {
      throw new Error(`Bot user ${botUsername} not found`);
    }

    // Share project with bot (write access)
    const shareResponse = await fetch(`${CONFIG.vikunja_api}/projects/${projectId}/users`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        user_id: botUser.id,
        right: 1  // 1 = write access
      })
    });

    if (!shareResponse.ok) {
      throw new Error(`Failed to share project: ${shareResponse.status}`);
    }

    return await shareResponse.json();
  }

  /**
   * Mark queue item as completed
   */
  async function markComplete(queueId) {
    const token = getToken();

    const response = await fetch(`${CONFIG.mcp_url}/project-queue/${queueId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      console.error(`[project-queue] Failed to mark ${queueId} complete:`, response.status);
    }
  }

  /**
   * Show notification to user
   */
  function showNotification(message, type = 'success') {
    if (!CONFIG.show_notifications) return;

    console.log(`[project-queue] ${type}: ${message}`);

    // Try to use Vikunja's notification system if available
    if (window.notify) {
      window.notify({
        type: type,
        text: message
      });
    }
  }

  /**
   * Process a single queue item
   */
  async function processQueueItem(item) {
    try {
      console.log(`[project-queue] Creating project: ${item.title}`);

      // Create project
      const project = await createProject(item);
      console.log(`[project-queue] Created project ${project.id}: ${project.title}`);

      // Share with bot
      if (item.bot_username) {
        await shareWithBot(project.id, item.bot_username);
        console.log(`[project-queue] Shared project ${project.id} with ${item.bot_username}`);
      }

      // Mark as completed
      await markComplete(item.id);

      showNotification(`Created project: ${item.title}`, 'success');
      return { success: true, project };

    } catch (error) {
      console.error(`[project-queue] Failed to process item ${item.id}:`, error);
      showNotification(`Failed to create project: ${item.title}`, 'error');
      return { success: false, error: error.message };
    }
  }

  /**
   * Process all pending queue items
   */
  async function processQueue() {
    const queue = await fetchQueue();

    if (queue.length === 0) {
      console.log('[project-queue] No pending projects');
      return;
    }

    console.log(`[project-queue] Processing ${queue.length} pending project(s)`);

    for (const item of queue) {
      await processQueueItem(item);
    }
  }

  /**
   * Initialize queue handler
   */
  function init() {
    if (CONFIG.poll_on_load) {
      // Run on page load
      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', processQueue);
      } else {
        processQueue();
      }
    }
  }

  // Export for manual triggering
  window.projectQueueHandler = {
    processQueue,
    fetchQueue,
    processQueueItem
  };

  // Auto-initialize
  init();
})();

