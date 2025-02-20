<p align="center">
<br />
    <img src="https://raw.githubusercontent.com/jeasonzhang-eth/AutoAlpha/refs/heads/master/image/auto_alpha.jpg" width="400" alt=""/>
<br />
</p>
<p align="center"><strong style="font-size: 24px;">Real-Time Crypto Data Harvesting with AI-Driven Trading Decisions On Aptos.</strong></p>
<p align="center" style="display: flex; justify-content: center; align-items: center;">
    <span style="display: inline-flex; align-items: center; background-color: #1c1c1c; padding: 5px; border-radius: 6px;">
        <img src="https://img.shields.io/github/stars/jeasonzhang-eth/AutoAlpha?style=social" alt="GitHub stars"/>
        <span style="margin: 0 10px; color: white; font-size: 14px;"></span>
        <a href="https://www.easya.io/">
            <img src="https://github.com/user-attachments/assets/09cfc307-f04f-4225-8c3b-bc96c47583a6" alt="EasyA" style="height: 21px;"/>
        </a>
    </span>
</p>

---

### **What is AutoAlpha?**

AutoAlpha revolutionizes decentralized trading by creating the one of best AI agent ecosystem that natively integrates Aptos blockchain analytics with Merkle Trade's leveraged trading infrastructure. This project addresses five critical challenges in crypto trading:

1. **Information Overload**: Traders struggle to process real-time market data, news sentiment, and on-chain analytics simultaneously.
2. **Execution Latency**: Manual trading creates 15-30s delays during market volatility, costing users an average of 2.8% ROI per trade.
3. **Multi-dimensional decision-making**: Traditional trading bots lack the capability to integrate on-chain data with real-time news for multi-dimensional decision-making.
4. **Opaque Risk Management**: 72% of DeFi users distrust traditional trading bots due to unverifiable decision logic.
5. **Lack of transparent AI trading infrastructure**: The DeFi sector lacks a verifiable and transparent AI trading infrastructure.

### **Technical Architecture**

![TechnicalArch](https://raw.githubusercontent.com/jeasonzhang-eth/AutoAlpha/refs/heads/master/image/AutoAlpha_TechnicalArch.jpg)

### **Features**

- Real-time price tracking
- News sentiment analysis
- AI-powered trade execution

### **Solution Architecture**:

#### **Part 1. Data Fetcher Module**

##### Prerequisites

```shell
# create a virtual environment
conda create -n auto_alpha
conda activate auto_alpha

# install dependency
pip install python-dotenv
pip install firecrawl-py
pip install langchain
pip install langchain_community
pip install sqlalchemy
```

##### 1. News Scraping

The News Scraping submodule utilizes FireCrawlLoader from LangChain to gather news data. The implementation includes three main modes of operation:

1. Scrape Mode:

- Extracts data from a single URL
- Converts content to LLM-ready markdown format
- Configurable with parameters like limit and format options

2. Crawl Mode:

- Recursively crawls the main URL and all accessible subpages
- Returns markdown content for each page
- Handles complex scenarios including reverse proxies and JavaScript-blocked content

3. Map Mode:

- Creates a semantic map of related pages
- Returns a structured list of connected content

Key Features:

- Environment variable management for API keys
- Built-in handling of rate limits and caching
- Support for multiple output formats (markdown, HTML)
- Asynchronous loading capabilities through lazy_load()
- Metadata extraction for each scraped page

The module leverages FireCrawl's API (developed by mendable.ai) to efficiently convert web content into formats suitable for LLM processing, requiring no sitemap for operation.

##### 2. Price Feed

The Price Feed submodule is a comprehensive system for fetching and managing cryptocurrency and fiat currency rates. It consists of three main components:

1. Database Models:

- CurrencyRate: Stores historical currency data
- CurrencyLatestRate: Maintains current currency rates
- Features include:
  * Currency code tracking
  * Rate and price storage
  * Currency type classification (fiat/crypto)
  * UTC timestamp management

2. DatabaseManager:

- Handles all database operations using SQLAlchemy
- Key functionalities:
  * Connection pool management
  * Rate saving with batch processing
  * Latest rate retrieval
  * Historical data querying
- Performance optimizations:
  * Query precompilation
  * Connection pooling
  * Batch insertions
  * Performance monitoring via timing decorator

3. CurrencyData System:

- Implements threaded data collection
- Components:
  * CurrencyDataWorker: Handles async API requests
  * Thread-safe rate updates
  * Separate handling for crypto and fiat currencies
- Features:
  * Queue-based data processing
  * Thread synchronization using locks
  * Automatic database updates
  * Real-time rate monitoring

The system uses environment variables for API configurations and implements error handling throughout all operations.

#### **Part 2: AI Agent Driven Trading Module**

- Built on ElizaOS framework
- Integrates Merkle Trade plugin for Aptos blockchain interactions
- Implements automated trading strategies based on analyzed data

### **Demo**

- [Demo ](https://www.youtube.com/watch?v=i1c7pYEDaY0)(20 Feb 2025)

### **Images**

<img width="1512" alt="img1" src="https://raw.githubusercontent.com/jeasonzhang-eth/AutoAlpha/refs/heads/master/image/auto_alpha-1.jpg">
<img width="1512" alt="img2" src="https://raw.githubusercontent.com/jeasonzhang-eth/AutoAlpha/refs/heads/master/image/auto_alpha-2.jpg">
<img width="1511" alt="img3" src="https://raw.githubusercontent.com/jeasonzhang-eth/AutoAlpha/refs/heads/master/image/auto_alpha-3.jpg">
<img width="1512" alt="img4" src="https://raw.githubusercontent.com/jeasonzhang-eth/AutoAlpha/refs/heads/master/image/auto_alpha-4.jpg">

### **Roadmap**

- [ ] Integration with additional data sources
- [ ] Enhanced AI models for better market prediction
- [ ] Support for more trading pairs
- [ ] Advanced risk management features
- [ ] Cross-chain expansion

### **Reference**

- [trendFinder](https://github.com/ericciarla/trendFinder)
- [Bitget API](https://www.bitget.com/zh-CN/api-doc/spot/intro)
- [Firecrawl](https://github.com/mendableai/firecrawl)
- [Merkle Trade ElizaOS Plugin & Sample AI Agents](https://github.com/merkle-trade/merkle-eliza-samples)
- [Merkle Trade Doc](https://docs.merkle.trade/)
- [ElizaOS](https://github.com/elizaOS/eliza)

## **Contributing & License**

Help us build AutoAlpha! AutoAlpha is an open-source software licensed under the [MIT License](https://github.com/jjjutla/melodot/blob/main/MIT-LICENSE.txt).



