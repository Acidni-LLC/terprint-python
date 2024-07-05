using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Terprint.Web.Migrations
{
    /// <inheritdoc />
    public partial class addtables : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "Grower",
                columns: table => new
                {
                    GrowerId = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Name = table.Column<string>(type: "nvarchar(max)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Grower", x => x.GrowerId);
                });

            migrationBuilder.CreateTable(
                name: "Matrixes",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Terpene = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Matrix = table.Column<int>(type: "int", nullable: false),
                    Row = table.Column<int>(type: "int", nullable: false),
                    Column = table.Column<int>(type: "int", nullable: false),
                    Color = table.Column<string>(type: "nvarchar(max)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Matrixes", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "RatingCategory",
                columns: table => new
                {
                    RatingCategoryId = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    CategoryName = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    CategoryDescription = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    CategoryTitle = table.Column<string>(type: "nvarchar(max)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_RatingCategory", x => x.RatingCategoryId);
                });

            migrationBuilder.CreateTable(
                name: "States",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    StateName = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    StateAbbreviation = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    StateCapital = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    StateRegion = table.Column<string>(type: "nvarchar(max)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_States", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "Strain",
                columns: table => new
                {
                    StrainId = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    StrainName = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    StrainDescription = table.Column<string>(type: "nvarchar(max)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Strain", x => x.StrainId);
                });

            migrationBuilder.CreateTable(
                name: "GrowerStates",
                columns: table => new
                {
                    GrowersGrowerId = table.Column<int>(type: "int", nullable: false),
                    StatesId = table.Column<int>(type: "int", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_GrowerStates", x => new { x.GrowersGrowerId, x.StatesId });
                    table.ForeignKey(
                        name: "FK_GrowerStates_Grower_GrowersGrowerId",
                        column: x => x.GrowersGrowerId,
                        principalTable: "Grower",
                        principalColumn: "GrowerId",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_GrowerStates_States_StatesId",
                        column: x => x.StatesId,
                        principalTable: "States",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "Batch",
                columns: table => new
                {
                    BatchId = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Name = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Type = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Date = table.Column<DateTime>(type: "datetime2", nullable: false),
                    GrowerId = table.Column<int>(type: "int", nullable: false),
                    StrainId = table.Column<int>(type: "int", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Batch", x => x.BatchId);
                    table.ForeignKey(
                        name: "FK_Batch_Grower_GrowerId",
                        column: x => x.GrowerId,
                        principalTable: "Grower",
                        principalColumn: "GrowerId",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_Batch_Strain_StrainId",
                        column: x => x.StrainId,
                        principalTable: "Strain",
                        principalColumn: "StrainId");
                });

            migrationBuilder.CreateTable(
                name: "Rating",
                columns: table => new
                {
                    RatingId = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    userid = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    OverallRating = table.Column<int>(type: "int", nullable: false),
                    Taste = table.Column<int>(type: "int", nullable: true),
                    Effect = table.Column<int>(type: "int", nullable: true),
                    Notes = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    BuyAgain = table.Column<bool>(type: "bit", nullable: false),
                    BatchId = table.Column<int>(type: "int", nullable: true),
                    RatingCategoryId = table.Column<int>(type: "int", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Rating", x => x.RatingId);
                    table.ForeignKey(
                        name: "FK_Rating_Batch_BatchId",
                        column: x => x.BatchId,
                        principalTable: "Batch",
                        principalColumn: "BatchId");
                    table.ForeignKey(
                        name: "FK_Rating_RatingCategory_RatingCategoryId",
                        column: x => x.RatingCategoryId,
                        principalTable: "RatingCategory",
                        principalColumn: "RatingCategoryId");
                });

            migrationBuilder.CreateTable(
                name: "TerpeneValues",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Grower = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Value = table.Column<double>(type: "float", nullable: false),
                    Material = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    TerpeneName = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Strain = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    BatchID = table.Column<int>(type: "int", nullable: false),
                    Rating = table.Column<double>(type: "float", nullable: false),
                    Scale = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Date = table.Column<DateOnly>(type: "date", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_TerpeneValues", x => x.Id);
                    table.ForeignKey(
                        name: "FK_TerpeneValues_Batch_BatchID",
                        column: x => x.BatchID,
                        principalTable: "Batch",
                        principalColumn: "BatchId",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "THCLevels",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Name = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Value = table.Column<double>(type: "float", nullable: false),
                    Scale = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    BatchId = table.Column<int>(type: "int", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_THCLevels", x => x.Id);
                    table.ForeignKey(
                        name: "FK_THCLevels_Batch_BatchId",
                        column: x => x.BatchId,
                        principalTable: "Batch",
                        principalColumn: "BatchId");
                });

            migrationBuilder.CreateIndex(
                name: "IX_Batch_GrowerId",
                table: "Batch",
                column: "GrowerId");

            migrationBuilder.CreateIndex(
                name: "IX_Batch_StrainId",
                table: "Batch",
                column: "StrainId");

            migrationBuilder.CreateIndex(
                name: "IX_GrowerStates_StatesId",
                table: "GrowerStates",
                column: "StatesId");

            migrationBuilder.CreateIndex(
                name: "IX_Rating_BatchId",
                table: "Rating",
                column: "BatchId");

            migrationBuilder.CreateIndex(
                name: "IX_Rating_RatingCategoryId",
                table: "Rating",
                column: "RatingCategoryId");

            migrationBuilder.CreateIndex(
                name: "IX_TerpeneValues_BatchID",
                table: "TerpeneValues",
                column: "BatchID");

            migrationBuilder.CreateIndex(
                name: "IX_THCLevels_BatchId",
                table: "THCLevels",
                column: "BatchId");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "GrowerStates");

            migrationBuilder.DropTable(
                name: "Matrixes");

            migrationBuilder.DropTable(
                name: "Rating");

            migrationBuilder.DropTable(
                name: "TerpeneValues");

            migrationBuilder.DropTable(
                name: "THCLevels");

            migrationBuilder.DropTable(
                name: "States");

            migrationBuilder.DropTable(
                name: "RatingCategory");

            migrationBuilder.DropTable(
                name: "Batch");

            migrationBuilder.DropTable(
                name: "Grower");

            migrationBuilder.DropTable(
                name: "Strain");
        }
    }
}
