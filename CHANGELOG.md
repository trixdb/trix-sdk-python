# Changelog

All notable changes to the Trix Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.6.0](https://github.com/trixdb/trix-sdk-python/compare/v0.5.0...v0.6.0) (2026-08-04)


### Features

* add batch_scan_code and analyze_code_complexity to GitHubResource ([e6409e6](https://github.com/trixdb/trix-sdk-python/commit/e6409e68d2470f2c3d05f7ccf5683c7cf0c57504))
* add build_ast_query and architecture_review to Python SDK ([1157247](https://github.com/trixdb/trix-sdk-python/commit/11572472bb1956b69d3b93b24c1d1102c6617c02))
* add CqlQuery model with CqlFromMode typing to Python SDK ([b6308bf](https://github.com/trixdb/trix-sdk-python/commit/b6308bfaadab97e1b7f1610dfcb8fae0a3e31698))
* add explain_code and suggest_refactoring to Python SDK ([3fd9323](https://github.com/trixdb/trix-sdk-python/commit/3fd93234366d43ca64b0b6c024421739da5a2f24))
* add get_active_branches to Python SDK (sync + async) ([8e08cbe](https://github.com/trixdb/trix-sdk-python/commit/8e08cbe83ba4992a32efcb6c07b50fb17e026182))
* add get_clean_code() to Python SDK (sync + async) ([cf6f611](https://github.com/trixdb/trix-sdk-python/commit/cf6f6110318ff302f64a57b3cd24cc0a67dfafc0))
* add get_design_patterns() to Python SDK (sync + async) ([2a50b95](https://github.com/trixdb/trix-sdk-python/commit/2a50b95b1c70a15237b23e4b454b4cecd21becc1))
* add get_function_profile() to Python SDK (sync + async) ([ce0b11d](https://github.com/trixdb/trix-sdk-python/commit/ce0b11db620de54f9f7fe21031b283c4bd84d4ed))
* add get_function_risk_delta method (CQL mode 81) ([ca4b7e9](https://github.com/trixdb/trix-sdk-python/commit/ca4b7e95a5e3b178b2f7dbb965b2463ac6277d82))
* add get_goal_progress_history (sync + async) + GoalProgressHistoryResponse type ([82caf42](https://github.com/trixdb/trix-sdk-python/commit/82caf427cd47aa54e8ec7d8b9d7997d98ed18324))
* add get_hotspot_matrix to Python SDK (iter 38) ([85b89ea](https://github.com/trixdb/trix-sdk-python/commit/85b89ea72bd14404cd551b764a1a035dd919e3f6))
* add get_module_cohesion method (CQL mode 80) ([e0b9616](https://github.com/trixdb/trix-sdk-python/commit/e0b96167c2f4c02b92b33df183a88b53c8489a90))
* add get_module_smell_heat to Python SDK (iter 40) ([23b9ff1](https://github.com/trixdb/trix-sdk-python/commit/23b9ff12ffbb6f8a5fcf4cf7a023e0d8c65a61fa))
* add get_refactor_priority to Python SDK (iter 39) ([2230fce](https://github.com/trixdb/trix-sdk-python/commit/2230fcedc198e1bf5feeb6680b5acb0d65662809))
* add get_smell_trend + get_coupling_analysis to Python SDK (iter 37) ([b2d106e](https://github.com/trixdb/trix-sdk-python/commit/b2d106ef136b1b0002833950d068250ca822763e))
* add get_testability + get_api_surface methods (CQL modes 78-79) ([cd55b9c](https://github.com/trixdb/trix-sdk-python/commit/cd55b9ce1329a72db86711590d7881f7ad385242))
* add get_testability() — CQL mode 78 (sync + async) ([a0396b8](https://github.com/trixdb/trix-sdk-python/commit/a0396b8a453b132e95f7de6df6a023ba63591427))
* add get_top_rules to Python SDK (iter 41) ([c31b516](https://github.com/trixdb/trix-sdk-python/commit/c31b516eb76b5c7de5958ac3463bd90f9d583ee8))
* add get_toxic_files + evaluate_quality_gate + trend/risk SDK methods ([e4ff67d](https://github.com/trixdb/trix-sdk-python/commit/e4ff67d2c957f69ff9c2e882a52cf668de7a1ab1))
* add pre_flight_pr method to sync and async GitHub client ([4e24993](https://github.com/trixdb/trix-sdk-python/commit/4e2499307050b187df6e44205f233206d2f8b918))
* add PRFileMetric model to PRReviewResult ([d8e15cc](https://github.com/trixdb/trix-sdk-python/commit/d8e15cc344bba78c2d6cf17c5d3476354a835fc2))
* add review_pr_code — AST-level PR code review with quality score and grade ([4e4ddb3](https://github.com/trixdb/trix-sdk-python/commit/4e4ddb37f132ea3db7c4d324cb18ff6f64c0d243))
* add scan_code() / async scan_code() + ScanCodeResult type to Python SDK ([8c96504](https://github.com/trixdb/trix-sdk-python/commit/8c96504fe998834be471f8be7d6c6978d817437f))
* add security_hotspots to CqlFromMode ([e9723ee](https://github.com/trixdb/trix-sdk-python/commit/e9723eece3e1bb1f6113465cddf2146f2b5f6965))
* add submit_pr_review and check_pr_quality_gate — SDK parity for PR review submission and gates ([cd3306d](https://github.com/trixdb/trix-sdk-python/commit/cd3306d480b60448cbb9772c4c04d0f2f0a76479))
* **ADR-109a:** add resolve_pipeline to Python SDK (tick 79) ([29d680b](https://github.com/trixdb/trix-sdk-python/commit/29d680b47887c2c754170f028e5d81bf9fc3de2d))
* **ADR-143:** add Trix.ping() / AsyncTrix.ping() health check ([3fed1f9](https://github.com/trixdb/trix-sdk-python/commit/3fed1f9561ee18e3030964293bbb3dae82c99dea))
* agent E2E test suite + agent stream types ([df49c74](https://github.com/trixdb/trix-sdk-python/commit/df49c74df1cc1140a515eda00116b9cd27117f76))
* **code:** add analyze_contributor_quality() to Python SDK (sync + async) ([ae91b25](https://github.com/trixdb/trix-sdk-python/commit/ae91b25cf0a45c4943ea6e4dbdacb88f97a010e5))
* **code:** add find_dead_code() to Python SDK (sync + async) ([8e8089e](https://github.com/trixdb/trix-sdk-python/commit/8e8089e236296c6d77efd6ad776a0737d1013c61))
* **code:** add get_abstraction_quality() to Python SDK (sync + async) ([4a5d802](https://github.com/trixdb/trix-sdk-python/commit/4a5d8024271606a15bfd37e621ebad00a27d3aa5))
* **code:** add get_function_outliers() to Python SDK (sync + async) ([000f9bd](https://github.com/trixdb/trix-sdk-python/commit/000f9bdd64ebf38bc7bed19d47cfb2d1c02abf52))
* **cql:** add 5 new CQL modes and query fields to Python SDK ([f2b9003](https://github.com/trixdb/trix-sdk-python/commit/f2b90039f595d015f159738c11e94afa933cbed9))
* **cql:** add refactor_candidates to CqlFromMode ([f636f4f](https://github.com/trixdb/trix-sdk-python/commit/f636f4f7a761232358eb36286b3684cbdae317a1))
* expand CqlFromMode literals and CqlQuery fields for new CQL modes ([0007043](https://github.com/trixdb/trix-sdk-python/commit/0007043eb88dcf0c687e6b004bdecfc97a69a67a))
* **github:** add agent_quality_scores + human_avg_quality to AgentAttributionResponse ([bc0d4eb](https://github.com/trixdb/trix-sdk-python/commit/bc0d4eb4d496cc400b4161e537bdfdb12684fd9e))
* **github:** add AgentAuditResult types + get_agent_audit_trail methods ([6df4fec](https://github.com/trixdb/trix-sdk-python/commit/6df4fecf3c663508f74f25006bd19a320a38dcc4))
* **github:** add ApprovedPR models and get_approved_prs methods ([1582ed0](https://github.com/trixdb/trix-sdk-python/commit/1582ed09d5586f9275dc65a299d19483532f82dc))
* **github:** add AssigneeCycleTimeResult types + get_assignee_cycle_time methods ([7fe4695](https://github.com/trixdb/trix-sdk-python/commit/7fe46954ed09dbd2ae0c58c41fcbfa8cad324a87))
* **github:** add CycleTimeTrendResult + get_cycle_time_trend (Phase 4) ([2507014](https://github.com/trixdb/trix-sdk-python/commit/2507014c6273e90f76540056e6ba1aa5fbe13c9b))
* **github:** add debt, quality-gate, CQL, review-pr, create-pr to Python SDK ([b819c72](https://github.com/trixdb/trix-sdk-python/commit/b819c72d553c2eec5128fde8146e9c6fd986f7ed))
* **github:** add detectConventions, generateTests, postReviewFindings, createFixPR, reviewDependencyChanges, analyzeChangeImpact methods + types ([875afab](https://github.com/trixdb/trix-sdk-python/commit/875afab3f90380a860cc3ae1066ca292d108b8b5))
* **github:** add get_issue_flow() sync and async — IssueFlowResult types ([2036c1b](https://github.com/trixdb/trix-sdk-python/commit/2036c1b10db0d43cff0f943fcee0c2e7e98a64a4))
* **github:** add get_issue_triage() method and IssueTriageResult types ([3d6748b](https://github.com/trixdb/trix-sdk-python/commit/3d6748b4f0681b0f6d3162f0adb9ce5cec5d0991))
* **github:** add get_pr_quality_trend — 12-week PR quality score trend ([e2d1cf6](https://github.com/trixdb/trix-sdk-python/commit/e2d1cf637037564b00756459a8e6e5f01d6a4aad))
* **github:** add get_pr_size_distribution to Python SDK (ADR-152) ([a5d5733](https://github.com/trixdb/trix-sdk-python/commit/a5d57336fe6e0562668806b3721e418f7bd95838))
* **github:** add get_review_stats and get_weekly_activity to async Python SDK ([d11b588](https://github.com/trixdb/trix-sdk-python/commit/d11b5882d635fdcd96c08441342ac8d58cd7af12))
* **github:** add get_review_stats and get_weekly_activity to Python SDK ([e1fcde2](https://github.com/trixdb/trix-sdk-python/commit/e1fcde280fd0acacba1e68dbb52f8ab8c0ad9ad2))
* **github:** add get_review_turnaround to Python SDK (ADR-152) ([890e9cc](https://github.com/trixdb/trix-sdk-python/commit/890e9cc3e59789ecfa9b38c55dd814cdfbd71fe3))
* **github:** add HealthSnapshotIssueFlow model + issueFlow field ([36b8db8](https://github.com/trixdb/trix-sdk-python/commit/36b8db8b0bd716a2f4f3b5f1939b2ff6611603b4))
* **github:** add issue cycle time types and methods (Phase 4) ([87a38f4](https://github.com/trixdb/trix-sdk-python/commit/87a38f4b8af894ee2e73a1e983f0d014dfcb236d))
* **github:** add issueBacklog + reviewCoverage to HealthSnapshotResponse ([2b911bb](https://github.com/trixdb/trix-sdk-python/commit/2b911bb9dbd04f488e808a9bf605f56e84e1f85c))
* **github:** add IssueBacklogResult models and get_issue_backlog methods ([6958212](https://github.com/trixdb/trix-sdk-python/commit/6958212ae8be5ba2693dc253184d9606b279a2e5))
* **github:** add IssueResolversResult + get_issue_resolvers (Phase 4) ([53d429a](https://github.com/trixdb/trix-sdk-python/commit/53d429a03546b9ac3d25a0596e2f9cf1210f0ab2))
* **github:** add IssueThroughput and SlowestCycleLabel to HealthSnapshotResponse ([97dc529](https://github.com/trixdb/trix-sdk-python/commit/97dc52994a03f91a0173b5acd4bf996529ca054e))
* **github:** add IssueThroughputResult + get_issue_throughput (Phase 4) ([d731445](https://github.com/trixdb/trix-sdk-python/commit/d731445b0f9604a5879350ed42c27b13ee96f1c6))
* **github:** add min/max_quality_score to get_pr_briefs (sync + async) ([4f37d19](https://github.com/trixdb/trix-sdk-python/commit/4f37d198f450020c5c2d4ca06034e98496ee40e4))
* **github:** add pr_quality_trend, review_turnaround, urgent_items to HealthSnapshotResponse ([942ce57](https://github.com/trixdb/trix-sdk-python/commit/942ce57b9055213daa41bade08a2090f38e471d4))
* **github:** add requested_reviewers + has_review to OpenPRAging model ([f4c9643](https://github.com/trixdb/trix-sdk-python/commit/f4c96435a1afe928900eb20c0a67d1cb1b34c0a6))
* **github:** add review network SDK support (Python sync + async) ([1877e4e](https://github.com/trixdb/trix-sdk-python/commit/1877e4e4f57e54427aa88cad845a872bb49c5e7d))
* **github:** add ReviewCoverageResult models and get_review_coverage methods ([a583ca2](https://github.com/trixdb/trix-sdk-python/commit/a583ca2d00141ba187088e6b2f7e4a4a63a4c401))
* **github:** add reviews_given + approvals to ContributorQualityStat ([fb65729](https://github.com/trixdb/trix-sdk-python/commit/fb657291ca49f7b0f1464b8c6694421a60a9ab8f))
* **github:** add ScopeCreepResult types + get_scope_creep methods ([c891160](https://github.com/trixdb/trix-sdk-python/commit/c8911601974816609e159978854b2cb8e04295b0))
* **github:** add SecurityFinding type and update PRReviewResult in Python SDK ([a4fe7ab](https://github.com/trixdb/trix-sdk-python/commit/a4fe7abb4f172e62f74d24cb27a0bfca08daa202))
* **github:** add WorkQueueResult models and get_work_queue() sync+async (ADR-152) ([c8d3f0f](https://github.com/trixdb/trix-sdk-python/commit/c8d3f0f962018ab8d0a412030abb8e2ca7e1b48e))
* **github:** AssigneeStat + IssueAssigneesResult models; get_issue_assignees() sync+async ([03de21b](https://github.com/trixdb/trix-sdk-python/commit/03de21b88bae7b17cd2b543b877d7570870b6314))
* **github:** CommitLeader + CommitLeadersResult models; get_commit_leaders() sync+async ([5750293](https://github.com/trixdb/trix-sdk-python/commit/575029346cbee47be4b36b22fca33a453dd628a4))
* **github:** ContributorMomentumResult types + get_contributor_momentum (sync + async) ([fd830a3](https://github.com/trixdb/trix-sdk-python/commit/fd830a354b613c2a9db75ad25bd6c4e8ee3b9bf2))
* **github:** get_ai_vs_human_quality — AI vs human code quality comparison ([7f2020c](https://github.com/trixdb/trix-sdk-python/commit/7f2020c097165c9694a713ba61ef4856e3bd06ec))
* **github:** get_bus_factor — knowledge concentration risk (ADR-152) ([69c353e](https://github.com/trixdb/trix-sdk-python/commit/69c353e67462602cedf3cdd1ba4efa21237b203c))
* **github:** get_dora_metrics — DORA engineering excellence metrics ([ce799fa](https://github.com/trixdb/trix-sdk-python/commit/ce799fadc0d555ce0b0d25773d4b7ae5d1fed444))
* **github:** get_pr_task_alignment — detect semantic drift between PRs and linked issues ([3dc01f6](https://github.com/trixdb/trix-sdk-python/commit/3dc01f67fc26b77ae1e9adfb8ef7f471e40cd5cd))
* **github:** get_review_depth — reviewer thoroughness analytics (Python) ([8ded587](https://github.com/trixdb/trix-sdk-python/commit/8ded5870f3dd250e6bb102368044551e2ccba2d1))
* **github:** get_test_gap — test coverage gap endpoint (ADR-152) ([359c55d](https://github.com/trixdb/trix-sdk-python/commit/359c55dda858cf45320912e413e688b89a5d28d5))
* **github:** LabelVelocity + LabelVelocityResult models; get_label_velocity() sync+async ([0742b4e](https://github.com/trixdb/trix-sdk-python/commit/0742b4ec55c19481bf98e7cf044bb8e8f36c59b6))
* **github:** MilestoneStat + MilestonesResult models; get_milestones() sync+async ([99e0fc9](https://github.com/trixdb/trix-sdk-python/commit/99e0fc9499707947cd7edaf8b111b988ca2ea629))
* **github:** PrMergeTimeResult types + get_pr_merge_time method (sync + async) ([166e2a2](https://github.com/trixdb/trix-sdk-python/commit/166e2a2dba723a6d0a93828b99c994218113976f))
* **github:** ReviewerWorkloadResult + get_reviewer_workload sync+async ([9a4dea5](https://github.com/trixdb/trix-sdk-python/commit/9a4dea59d4fa1e23b2ffe0a7d9d23e17af1f4293))
* **github:** update ReleaseReadinessResponse — richer structure (blockers, hotspots, stale PRs) ([3f7935f](https://github.com/trixdb/trix-sdk-python/commit/3f7935fadfc49f0e06687fb96649562e1ece85cb))
* **P10:** Python SDK account-default pipeline methods ([ab18337](https://github.com/trixdb/trix-sdk-python/commit/ab18337f1ed8f5f4d8eed215f379654eef704fe8))
* **P10:** Python SDK space-default pipeline methods (sync + async) ([203c513](https://github.com/trixdb/trix-sdk-python/commit/203c513538ca2d869b7bfef1d8e8f66fcbcaa08a))
* **P10:** Python SDK trigger methods for session/mega/scoped ([5d874bd](https://github.com/trixdb/trix-sdk-python/commit/5d874bd770ff224399b96f833e7c7951211ce67d))
* PRReviewResult gains quality_score field (0-100, default 100) ([20a0305](https://github.com/trixdb/trix-sdk-python/commit/20a030585f2fcb3b0abad6a70e6884d1538a4269))
* **sdk-py:** add 6 new code health methods + types (session 15-16 parity) ([570fdf5](https://github.com/trixdb/trix-sdk-python/commit/570fdf5380a3ec355775e9d9f2f2f37ec0c02694))
* **sdk-py:** add get_health_snapshot method + HealthSnapshotResponse types ([2af8e30](https://github.com/trixdb/trix-sdk-python/commit/2af8e3057896d500c848beb96144926f0d3011f7))
* **sdk-py:** add get_pr_briefs method + PRBrief/PRBriefsResponse types ([fe234ea](https://github.com/trixdb/trix-sdk-python/commit/fe234ea5c27252dcbc51caec815dc56b187148dc))
* **sdk-py:** add GitHubResource sync+async — ADR-152 Phases 1–2 ([477f202](https://github.com/trixdb/trix-sdk-python/commit/477f2027e5f32988bd3ce7bcf683aa0e0cb416db))
* **sdk-py:** add pr_url field to PRBrief model ([484740f](https://github.com/trixdb/trix-sdk-python/commit/484740ff224267aa74b07e2ca2261e4b47b0e59f))
* **sdk-py:** add score to QualityGate + last_scanned_at to CodeSummaryResult ([4057e09](https://github.com/trixdb/trix-sdk-python/commit/4057e093d88a6497c15a681f0f4d428936517b28))
* **sdk-python:** add batch_search, knowledge_summary, store_and_organize, suggest_strategy methods ([5384967](https://github.com/trixdb/trix-sdk-python/commit/53849671def216de71b4c7aa295f78d3fd286d9b))
* **sdk-python:** add complexity_trend, contributor_risk, smell_density, pre_pr_checklist (iter 34) ([916a940](https://github.com/trixdb/trix-sdk-python/commit/916a9409a401487d2d295c476520dbdc00ad4657))
* **sdk-python:** add DepVuln type + extend PRReviewResult fields ([e6b9335](https://github.com/trixdb/trix-sdk-python/commit/e6b93353b1c9b8b362ef7abeff41dc18929ed574))
* **sdk-python:** add get_action_plan — ActionPlanResult types and sync/async methods ([bd7e374](https://github.com/trixdb/trix-sdk-python/commit/bd7e37424b0e2a8508143a8e0e5dafedc9f6ec96))
* **sdk-python:** add get_naming_violations (sync + async) ([14eb583](https://github.com/trixdb/trix-sdk-python/commit/14eb5836fd0fa578f06a365221cfbee1f12a1067))
* **sdk-python:** add get_project_health_score + get_test_smell (iter 36) ([330dcec](https://github.com/trixdb/trix-sdk-python/commit/330dcec249421b328b4647cb3c93ff8e018ed7ef))
* **sdk-python:** add get_solid_analysis (sync + async) — SOLID violations ([43af290](https://github.com/trixdb/trix-sdk-python/commit/43af2901793cb6a395beead8887bd3e677f01094))
* **sdk-python:** add get_tech_debt sync/async — TechDebtResult, TechDebtCategory types ([e039d1a](https://github.com/trixdb/trix-sdk-python/commit/e039d1af540e6813781e1e8e0568ee3c96f86feb))
* **sdk-python:** add Phase 5 methods to AsyncGitHubResource + extract types ([8b11cec](https://github.com/trixdb/trix-sdk-python/commit/8b11cec3f6227d75f5c6e4dd2c4ff0ad9f7d6c4b))
* **sdk-python:** custom rule CRUD sync+async — list/create/update/delete/test ([dbded5b](https://github.com/trixdb/trix-sdk-python/commit/dbded5b1f64b1f56d84049311bb2a6a3da2f9788))
* **sdk-python:** file_path filter + create_issue_from_suggestion ([d54909b](https://github.com/trixdb/trix-sdk-python/commit/d54909b3c485165c9bf0b145e5c15629bf0a9088))
* **sdk/python:** agent filter param for get_pr_briefs (sync + async) ([09618f2](https://github.com/trixdb/trix-sdk-python/commit/09618f258b4963de68e085760d91186bc5029c91))
* **sdk:** add avg_merge_days to ContributorQualityStat ([a58fefc](https://github.com/trixdb/trix-sdk-python/commit/a58fefce12abf2f2200dce4670b0b8a0cf157a46))
* **sdk:** add dead_code_ratio method (CQL mode 87) ([c3578a1](https://github.com/trixdb/trix-sdk-python/commit/c3578a10da6aeee341771f982b447a2bf5dc21ab))
* **sdk:** add get_contributor_quality to Python SDK ([a5072f2](https://github.com/trixdb/trix-sdk-python/commit/a5072f22c1044e70a44c141c5cf371cb582d3fdb))
* **sdk:** add get_pr_aging to Python SDK ([760831b](https://github.com/trixdb/trix-sdk-python/commit/760831bf464df37d96a009127270471022e92f34))
* **sdk:** add get_week_over_week — 7-day velocity comparison ([c48e1e2](https://github.com/trixdb/trix-sdk-python/commit/c48e1e2f6ff23ad6cad25b45c7e2365e8009926c))
* **sdk:** add scope_analysis method (CQL mode 86) ([294dd2c](https://github.com/trixdb/trix-sdk-python/commit/294dd2cb66c41799ed7f80c57867059e1b07d2fb))
* **types:** add agent field to PRBrief ([0a5b4a2](https://github.com/trixdb/trix-sdk-python/commit/0a5b4a23435599cb2daf9b603be6d3554cbf5522))
* **types:** add DesignFinding model and design field to AnalyzeCodeComplexityResult ([46f070b](https://github.com/trixdb/trix-sdk-python/commit/46f070b7bd8b6ff445290f6fbdfb3ab84da7e6ee))
* **types:** add file_report to CqlFromMode ([2e70b2b](https://github.com/trixdb/trix-sdk-python/commit/2e70b2b7c6ff88b6ef05ca4595ebdea37dd0fb59))
* **types:** add FunctionComplexityMetric + enrich FileComplexityMetric ([fbf9ce1](https://github.com/trixdb/trix-sdk-python/commit/fbf9ce18c62c31f367ece13ffa0b80bfb1853bd0))
* **types:** add symbols to CqlFromMode ([73713b7](https://github.com/trixdb/trix-sdk-python/commit/73713b7a9d63cdae28767f6f8b8765e408ed9e3f))
* **types:** add tech_debt to CqlFromMode and DesignFinding model ([0289939](https://github.com/trixdb/trix-sdk-python/commit/028993949fa9b89d8c8a82d26a0fd61ddd0b1300))
* **types:** add trend to CqlFromMode ([723b4e2](https://github.com/trixdb/trix-sdk-python/commit/723b4e201c94303ff7b851dc0b33bbc4bdde6bc8))
* **types:** add worst_functions to CqlFromMode ([1e90981](https://github.com/trixdb/trix-sdk-python/commit/1e9098146256eb2f32b762db77ecd3f7eb70b454))


### Bug Fixes

* **ADR-145:** align relationships.create() with REST wire contract ([2ba65dc](https://github.com/trixdb/trix-sdk-python/commit/2ba65dc607df5f8bf51683ccb0a8076028ec7b29))
* **client:** idempotency key so retries don't duplicate writes ([#7](https://github.com/trixdb/trix-sdk-python/issues/7)) ([#16](https://github.com/trixdb/trix-sdk-python/issues/16)) ([84d356d](https://github.com/trixdb/trix-sdk-python/commit/84d356de08a6c26a67e618a70e066dbf6a0a459c))
* **client:** send multipart Content-Type for file uploads ([#6](https://github.com/trixdb/trix-sdk-python/issues/6)) ([#15](https://github.com/trixdb/trix-sdk-python/issues/15)) ([9fccbbf](https://github.com/trixdb/trix-sdk-python/commit/9fccbbf5ce089e62e08fb91109bd6bdb302ed307))
* **docs:** Correct PyPI package name and GitHub repo URLs for public release ([#24](https://github.com/trixdb/trix-sdk-python/issues/24)) ([541e617](https://github.com/trixdb/trix-sdk-python/commit/541e617ba1afa9974927a5db8492ca23d514e546))
* format organize.py and core.py with black ([e7f6805](https://github.com/trixdb/trix-sdk-python/commit/e7f6805e9d4ddc8793ec662695894248b9ca259f))
* **github:** add get/post/put/patch/delete client verb helpers ([#5](https://github.com/trixdb/trix-sdk-python/issues/5)) ([#14](https://github.com/trixdb/trix-sdk-python/issues/14)) ([93f1208](https://github.com/trixdb/trix-sdk-python/commit/93f1208aaf4c95eed77116e1642f3d656685e1c9))
* **http:** Honor configured retryable exceptions in the retry loop ([#20](https://github.com/trixdb/trix-sdk-python/issues/20)) ([eb9fd2d](https://github.com/trixdb/trix-sdk-python/commit/eb9fd2d1d55b84d47a4f1bd1ef20ddef83aa33c7)), closes [#8](https://github.com/trixdb/trix-sdk-python/issues/8)
* **packaging:** single-source version and ship py.typed ([#9](https://github.com/trixdb/trix-sdk-python/issues/9)) ([#17](https://github.com/trixdb/trix-sdk-python/issues/17)) ([6f9834b](https://github.com/trixdb/trix-sdk-python/commit/6f9834b7c42b506d2d29b0a5c3684d39303305d2))
* **resources:** Add async multipart upload to AsyncFilesResource ([#19](https://github.com/trixdb/trix-sdk-python/issues/19)) ([9fc8c26](https://github.com/trixdb/trix-sdk-python/commit/9fc8c2687b39bfeb0e91db2976366397165848ab)), closes [#10](https://github.com/trixdb/trix-sdk-python/issues/10)
* **resources:** Raise typed errors on failed streaming bot runs ([#21](https://github.com/trixdb/trix-sdk-python/issues/21)) ([0f46db2](https://github.com/trixdb/trix-sdk-python/commit/0f46db2e0bbdfcea48937ffb1653c0ceacd57257)), closes [#11](https://github.com/trixdb/trix-sdk-python/issues/11)
* **resources:** Repair SDK methods that miss or mismatch backend routes ([#25](https://github.com/trixdb/trix-sdk-python/issues/25)) ([204e828](https://github.com/trixdb/trix-sdk-python/commit/204e8283500a9af670997366a86503e6eb69dd0c))
* **sdk:** prepend /v1 in transport + correct bots/personas/facts/entities namespaces (404/410 on most calls) ([#3](https://github.com/trixdb/trix-sdk-python/issues/3)) ([54d4ed9](https://github.com/trixdb/trix-sdk-python/commit/54d4ed92d9c58a763d4853a814d0e16dd14c4165))
* **types:** Re-export the full trix.types surface from the package root ([#23](https://github.com/trixdb/trix-sdk-python/issues/23)) ([0061c9e](https://github.com/trixdb/trix-sdk-python/commit/0061c9e9e6768f0b4e253e6d097ec5568c6b3787))

## [Unreleased]

### Fixed
- **GitHub resources**: ~144 `client.github.*` methods (e.g. `get_issue_cycle_time`,
  `dead_code_ratio`, `generate_tests`) raised `AttributeError` at call time because they
  invoked `self._client.get/post/put/patch/delete`, which the client never implemented.
  Added these verb helpers to the sync (`Trix`) and async (`AsyncTrix`) clients and to the
  client protocols, so every GitHub method now issues its request and returns the typed
  model. ([#5](https://github.com/trixdb/trix-sdk-python/issues/5))
- **Multipart uploads**: file uploads (e.g. `client.files.upload`, image/audio memory
  uploads) were sent with `Content-Type: application/json` instead of
  `multipart/form-data`, so the server could not parse the body. `_get_headers()` baked
  `Content-Type` into the `httpx` client-level defaults, which overrode the per-request
  multipart boundary. `Content-Type` is now left unset on the client and derived per
  request by httpx from the `json=` / `files=` body. ([#6](https://github.com/trixdb/trix-sdk-python/issues/6))
- **Idempotent retries**: the client auto-retries 5xx / 429 responses on all methods, which
  could duplicate a write when a mutating request's first attempt reached the server but the
  response was lost. Mutating requests (POST/PUT/PATCH/DELETE) now send a single stable
  `Idempotency-Key` (generated once, before the retry loop, reused across attempts) so the
  backend dedupes retries. GET and other non-mutating methods send no key; a caller-supplied
  key is preserved. ([#7](https://github.com/trixdb/trix-sdk-python/issues/7))
- **Packaging**: the version was duplicated across five places (pyproject.toml,
  `trix.__version__`, package.json, .release-please-manifest.json, and the built dist) and
  they disagreed (0.1.1 vs 0.5.0 vs 0.6.0). The version is now single-sourced: pyproject.toml
  is authoritative and `trix.__version__` is read from the installed distribution metadata,
  so runtime and dist always match. package.json and .release-please-manifest.json are
  realigned to the authoritative version.
- **Typing**: added `src/trix/py.typed` and declared it as package data so the PEP 561 marker
  ships in the wheel; downstream type checkers now treat `trix` as typed. ([#9](https://github.com/trixdb/trix-sdk-python/issues/9))

## [1.0.0] - 2025-12-25

### Added

#### Core Features
- Initial release of Trix Python SDK
- Full support for Trix API v1
- Synchronous client (`Trix`) and asynchronous client (`AsyncTrix`)
- Context manager support for both sync and async clients
- Comprehensive type hints using Pydantic models

#### Resources
- **Memories**: Full CRUD operations, bulk operations, audio transcription
- **Relationships**: Create, update, delete, and reinforce relationships
- **Clusters**: Manage clusters, add/remove memories, cluster expansion
- **Spaces**: Workspace organization and management
- **Graph**: Graph traversal, context retrieval, shortest path finding
- **Search**: Semantic and keyword search, embedding generation
- **Webhooks**: Event notifications and webhook management
- **Agent**: Session management and memory consolidation
- **Feedback**: Search result feedback and relationship creation
- **Highlights**: Text highlighting and auto-extraction
- **Jobs**: Background job monitoring and management

#### Developer Experience
- Automatic retry with exponential backoff for rate limits
- Comprehensive error handling with custom exception types
- Pagination helpers with automatic iteration
- Type-safe request and response models
- Detailed logging support
- Full IDE autocomplete support

#### Documentation
- Comprehensive README with examples
- API documentation in docstrings
- Example scripts for common use cases
- Contributing guidelines

#### Testing
- Unit tests for core functionality
- Integration test structure
- GitHub Actions CI/CD pipeline
- Code coverage reporting

### Technical Details
- Minimum Python version: 3.9
- Built on httpx for HTTP requests
- Pydantic v2 for data validation
- Support for both API key and JWT authentication

[Unreleased]: https://github.com/trixdb/trix-sdk-python/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/trixdb/trix-sdk-python/releases/tag/v1.0.0
