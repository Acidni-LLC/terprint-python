/****** Object:  Table [dbo].[terpeneResults]    Script Date: 10/5/2025 11:44:11 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].cannabinoidResults(
	[cannabinoidResultId] [int] IDENTITY(1,1) NOT NULL,
	[batch] [nvarchar](50) NULL,
	[Index] [int] NULL,
	Cannabinoid [nvarchar](50) NULL,
	[percent] [float] NULL,
	milligrams [float] NULL,
	[created] [datetime] NULL,
	[dispensaryId] [int] NULL,
	[createdBy] [nvarchar](50) NULL
) ON [PRIMARY]
GO


