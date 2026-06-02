<script>
  import { auth } from '../stores/auth.svelte.js'
  import { toast } from '../stores/toast.svelte.js'
  import { getAllOrders, getMyOrders } from '../services/api.js'

  let orders = $state([])
  let loading = $state(true)
  let expanded = $state(new Set())

  const stats = $derived({
    total: orders.length,
    revenue: orders.reduce((s, o) => s + o.total, 0),
    avgTicket: orders.length ? orders.reduce((s, o) => s + o.total, 0) / orders.length : 0,
    today: orders.filter(o => new Date(o.createdAt).toDateString() === new Date().toDateString()).length,
  })

  $effect(() => {
    if (auth.isAuthenticated) load()
  })

  async function load() {
    loading = true
    try {
      orders = auth.isAdmin ? await getAllOrders(auth.token) : await getMyOrders(auth.token)
    } catch (e) {
      toast.error('Error al cargar pedidos: ' + e.message)
    } finally {
      loading = false
    }
  }

  function toggle(id) {
    const next = new Set(expanded)
    next.has(id) ? next.delete(id) : next.add(id)
    expanded = next
  }

  function fmt(iso) {
    return new Date(iso).toLocaleString('es-ES', {
      day: '2-digit', month: 'short', year: 'numeric',
      hour: '2-digit', minute: '2-digit',
    })
  }
</script>

<div class="page">
  <div class="page__header">
    <div>
      <h1 class="page__title">{auth.isAdmin ? 'Gestión de Pedidos' : 'Mis Pedidos'}</h1>
      <p class="page__sub">
        {auth.isAdmin ? 'Todos los pedidos realizados en la plataforma' : 'Historial de tus compras'}
      </p>
    </div>
  </div>

  {#if auth.isAdmin}
    <div class="stats-row">
      <div class="stat-card">
        <span class="stat-card__label">Total pedidos</span>
        <span class="stat-card__value">{stats.total}</span>
      </div>
      <div class="stat-card stat-card--accent">
        <span class="stat-card__label">Ingresos totales</span>
        <span class="stat-card__value">{stats.revenue.toFixed(2)} EUR</span>
      </div>
      <div class="stat-card">
        <span class="stat-card__label">Ticket medio</span>
        <span class="stat-card__value">{stats.avgTicket.toFixed(2)} EUR</span>
      </div>
      <div class="stat-card">
        <span class="stat-card__label">Hoy</span>
        <span class="stat-card__value">{stats.today}</span>
      </div>
    </div>
  {/if}

  {#if loading}
    <div class="skeleton-list">
      {#each Array(4) as _}
        <div class="skeleton-row"></div>
      {/each}
    </div>
  {:else if orders.length === 0}
    <div class="empty-state">
      <div class="empty-icon">📦</div>
      <h2>Sin pedidos aún</h2>
      <p>{auth.isAdmin ? 'Ningún usuario ha realizado pedidos todavía.' : 'Aún no has realizado ninguna compra.'}</p>
    </div>
  {:else}
    <div class="orders-list">
      {#each orders as order (order._id)}
        <div class="order-card">
          <button class="order-header" onclick={() => toggle(order._id)}>
            <div class="order-header__left">
              <span class="order-id">#{order._id.slice(-6).toUpperCase()}</span>
              {#if auth.isAdmin}
                <span class="order-user">{order.username}</span>
              {/if}
              <span class="order-date">{fmt(order.createdAt)}</span>
            </div>
            <div class="order-header__right">
              <span class="order-items-count">{order.items.length} art.</span>
              <span class="order-total">{order.total.toFixed(2)} EUR</span>
              <span class="order-chevron {expanded.has(order._id) ? 'order-chevron--open' : ''}">›</span>
            </div>
          </button>

          {#if expanded.has(order._id)}
            <div class="order-body">
              <table class="items-table">
                <thead>
                  <tr>
                    <th>Producto</th>
                    <th>Precio unit.</th>
                    <th>Cantidad</th>
                    <th>Subtotal</th>
                  </tr>
                </thead>
                <tbody>
                  {#each order.items as item (item._id)}
                    <tr>
                      <td class="item-name">{item.productName}</td>
                      <td>{item.productPrice.toFixed(2)} EUR</td>
                      <td><span class="qty-badge">×{item.quantity}</span></td>
                      <td class="item-subtotal">{(item.productPrice * item.quantity).toFixed(2)} EUR</td>
                    </tr>
                  {/each}
                </tbody>
              </table>
              <div class="order-footer">
                <span>Total del pedido</span>
                <strong class="order-footer__total">{order.total.toFixed(2)} EUR</strong>
              </div>
            </div>
          {/if}
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .page {
    padding: 2rem;
    max-width: 1000px;
    margin: 0 auto;
    animation: fadeIn 0.3s ease;
  }

  .page__header {
    margin-bottom: 2rem;
  }

  .page__title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.5rem;
    letter-spacing: 0.04em;
    color: var(--text-primary);
    margin: 0;
    line-height: 1;
  }

  .page__sub {
    color: var(--text-muted);
    margin: 0.5rem 0 0;
    font-size: 0.95rem;
  }

  /* Stats */
  .stats-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
  }

  .stat-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .stat-card--accent {
    border-color: rgba(255, 87, 34, 0.3);
    background: rgba(255, 87, 34, 0.05);
  }

  .stat-card__label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.75rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-weight: 600;
  }

  .stat-card__value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.9rem;
    color: var(--text-primary);
    letter-spacing: 0.03em;
    line-height: 1;
  }

  .stat-card--accent .stat-card__value {
    color: var(--accent);
  }

  /* Orders list */
  .orders-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .order-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    overflow: hidden;
    transition: border-color 0.2s;
  }

  .order-card:hover {
    border-color: var(--border-hover);
  }

  .order-header {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.1rem 1.5rem;
    background: none;
    border: none;
    color: inherit;
    cursor: pointer;
    gap: 1rem;
    transition: background 0.15s;
  }

  .order-header:hover {
    background: rgba(255, 255, 255, 0.03);
  }

  .order-header__left {
    display: flex;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
  }

  .order-id {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    font-weight: 700;
    color: var(--accent);
    background: rgba(255, 87, 34, 0.1);
    padding: 0.25rem 0.6rem;
    border-radius: 6px;
  }

  .order-user {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text-primary);
  }

  .order-date {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.8rem;
    color: var(--text-muted);
  }

  .order-header__right {
    display: flex;
    align-items: center;
    gap: 1rem;
    flex-shrink: 0;
  }

  .order-items-count {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: var(--text-muted);
    background: rgba(255, 255, 255, 0.05);
    padding: 0.2rem 0.5rem;
    border-radius: 100px;
  }

  .order-total {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.25rem;
    color: var(--text-primary);
    letter-spacing: 0.03em;
  }

  .order-chevron {
    font-size: 1.4rem;
    color: var(--text-muted);
    transition: transform 0.2s;
    line-height: 1;
  }

  .order-chevron--open {
    transform: rotate(90deg);
  }

  /* Order body */
  .order-body {
    border-top: 1px solid var(--border);
    padding: 1.25rem 1.5rem;
  }

  .items-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.875rem;
    margin-bottom: 1rem;
  }

  .items-table th {
    text-align: left;
    color: var(--text-muted);
    font-weight: 600;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 0.5rem 0.75rem 0.75rem;
    border-bottom: 1px solid var(--border);
  }

  .items-table td {
    padding: 0.6rem 0.75rem;
    color: var(--text-primary);
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
  }

  .items-table tr:last-child td {
    border-bottom: none;
  }

  .item-name {
    font-weight: 600;
  }

  .item-subtotal {
    font-weight: 700;
    color: var(--accent);
  }

  .qty-badge {
    background: rgba(255, 255, 255, 0.07);
    border: 1px solid var(--border);
    padding: 0.15rem 0.5rem;
    border-radius: 100px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: var(--text-muted);
  }

  .order-footer {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    gap: 1.5rem;
    padding-top: 0.75rem;
    border-top: 1px solid var(--border);
    color: var(--text-muted);
    font-size: 0.9rem;
    font-family: 'DM Sans', sans-serif;
  }

  .order-footer__total {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.4rem;
    color: var(--text-primary);
    letter-spacing: 0.03em;
  }

  /* Empty */
  .empty-state {
    text-align: center;
    padding: 5rem 2rem;
    color: var(--text-muted);
  }

  .empty-icon {
    font-size: 3.5rem;
    opacity: 0.25;
    margin-bottom: 1rem;
  }

  .empty-state h2 {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0 0 0.5rem;
  }

  .empty-state p {
    font-size: 0.875rem;
    margin: 0;
  }

  /* Skeleton */
  .skeleton-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .skeleton-row {
    height: 64px;
    border-radius: 14px;
    background: var(--surface);
    animation: shimmer 1.5s infinite;
  }

  @keyframes shimmer {
    0%, 100% { opacity: 0.5; }
    50% { opacity: 1; }
  }

  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: translateY(0); }
  }
</style>
